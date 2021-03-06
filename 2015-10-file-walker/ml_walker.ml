(* Ocaml implementation of file walker *)

open Unix


let walk root dir_cb file_cb error_cb =
  let isdir st =
    st.st_kind == S_DIR
  and add_dir counts =
    match counts with (dirs, files, errors) -> (dirs+1, files, errors)
  and add_file counts =
    match counts with (dirs, files, errors) -> (dirs, files+1, errors)
  and add_error counts =
    match counts with (dirs, files, errors) -> (dirs, files, errors+1)
  in let rec iterate_directory handle dname work_q counts =
    (* Go through all the entries of one directory that's been opened. We
       call the callbacks, add to the counts, and add directories to the work q. *)
    try
      match readdir handle with
        "."
        | ".." -> iterate_directory handle dname work_q counts
        | file ->
           let p = dname ^ "/" ^ file in
           let (work_q, counts) =
             try
               let st = lstat p in
                 if isdir st then (dir_cb p st; (p::work_q, add_dir counts))
                 else (file_cb p st; (work_q, add_file counts))
             with Unix_error (code, fname, param) ->
               error_cb dname (error_message code); (work_q, add_error counts)
           in
             iterate_directory handle dname work_q counts
    with End_of_file -> closedir handle; (work_q, counts)
       | Unix_error (code, fname, param) ->
          (* If we get this exception here, it means that
                   the readdir had a problem. We will exit our loop
                   and attribute the error to the parent directory.*)
          closedir handle; error_cb dname (error_message code); (work_q, add_error counts)
  in let rec walk_dirs work_q counts =
       (* Pick a directory out of the work queue and process the files/entries.
          Then call walk_dirs recursively to process the rest of the queue. *)
       match work_q with
         dname::rest ->
           let work_q, counts =
             try
               let handle = opendir dname in
                 iterate_directory handle dname rest counts
             with Unix_error (code, fname, param) ->
                  (* Unable to open dname as a directory *)
                  error_cb dname (error_message code); (rest, add_error counts)
           in
             walk_dirs work_q counts
        | [] -> counts
  in let (st:stats) = handle_unix_error lstat root
     in
       dir_cb root st; walk_dirs (root::[]) (1, 0, 0)
;;                                           

let dir_cb path stat =
  () (*Printf.printf "Directory %s\n" path*)
let file_cb path stat =
  () (*Printf.printf "Directory %s\n" path*)
let error_cb path err =
  () (*Printf.printf "Error at %s: %s\n" path err*)
;;

let run root iterations dir_cb file_cb error_cb =
  (* Run for the specified number of iterations and print the last set of results *)
  let abs_root = FilePath.make_absolute (Sys.getcwd ()) root
  and result = ref (0, 0, 0) in
    for i = 1 to iterations do
      Printf.printf "Iteration %d" i; print_newline ();
      result := walk abs_root dir_cb file_cb error_cb
    done;
    !result
;;                   

match Array.length Sys.argv with
  | 2 -> let root =  Array.get Sys.argv 1 in
           let (dirs, files, errors) = run root 1 dir_cb file_cb error_cb in
             Printf.printf "%d directories, %d files, %d errors\n" dirs files errors
  | 3 -> let root = Array.get Sys.argv 1
         and iterations = int_of_string (Array.get Sys.argv 2) in
           let (dirs, files, errors) = run root iterations dir_cb file_cb error_cb in
             Printf.printf "%d directories, %d files, %d errors\n" dirs files errors
  | _ -> Printf.printf "%s ROOT_DIRECTORY\n" (Array.get Sys.argv 0)
;;

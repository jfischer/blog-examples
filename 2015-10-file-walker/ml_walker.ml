open Unix

let statdir base dirs fcnt =
  let dirhandle = handle_unix_error opendir base and
      dirs_r = ref dirs and
      fcnt_r = ref fcnt and
      files_r = ref [] in
    begin
      try
        while true do
          let file = readdir dirhandle in
            match file with
             | "." -> ()
             | ".." -> ()
             | _ -> let p = base ^ "/" ^ file in
                    let st = lstat p in
                    let isdir = st.st_kind == S_DIR in
                      if isdir then dirs_r := (p, st)::!dirs_r
                      else files_r := (p, st)::!files_r; fcnt_r := !fcnt_r + 1
        done
      with
        | End_of_file -> ()
    end;
    closedir dirhandle;
    (!dirs_r, !fcnt_r, !files_r)
;;

let walk base =
  let rec walker base dirs fcnt dcnt =
    let (dirs, fcnt, files) = statdir base dirs fcnt in
      match dirs with
        | [] -> (fcnt, dcnt)
        | (d, st)::rest -> walker d rest fcnt (dcnt+1)
  in walker base [] 0 0
;;

match Array.length Sys.argv with
  | 2 -> let root =  Array.get Sys.argv 1 in
         let (fcnt, dcnt) = walk root in
           Printf.printf "%d files, %d directories\n" fcnt dcnt
  | _ -> Printf.printf "%s ROOT_DIRECTORY\n" (Array.get Sys.argv 0)

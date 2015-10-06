package main

import "fmt"
import "os"
import "path/filepath"
import "syscall"
import "strconv"
//import "time"

type Filer interface {
	file_attributes(string, syscall.Stat_t)
	directory_attributes(string, syscall.Stat_t)
	error(string, error)
}


type Callbacks struct {
}
func (*Callbacks) file_attributes(path string, stats syscall.Stat_t) {
	//fmt.Printf("File %s\n", path)
}
func (*Callbacks) directory_attributes(path string, stats syscall.Stat_t) {
	//fmt.Printf("Directory %s\n", path)
}
func (*Callbacks) error(path string, err error) {
	//fmt.Printf("Error %s: %s\n", path, err)
}


func walk(root string, cb Filer) (int, int, int) {
	filecnt := 0
	dircnt := 1
	errcnt := 0
	var stats syscall.Stat_t
	err := syscall.Lstat(root, &stats)
	if err != nil {
		cb.error(root, err);
		return 0, 0, 1
	}
	cb.directory_attributes(root, stats);
	var work_q []string
	var dir string
	var files []string
	work_q = make([]string, 1, 10)
	work_q[0] = root
	for len(work_q) > 0 {
		dir, work_q = work_q[len(work_q)-1], work_q[:len(work_q)-1]
		dirfile, err := os.Open(dir)
		if err != nil {
			cb.error(dir, err)
			errcnt += 1
			continue
		}
		// Would like to use defer here, but it only works in a separate
		// function!
		//defer dirfile.Close()
		files, err = dirfile.Readdirnames(-1)
		if err != nil {
			cb.error(dir, err)
			errcnt+= 1
			dirfile.Close()
			continue
		}
		for _, filename := range files {
			var path = filepath.Join(dir, filename)
			err = syscall.Lstat(path, &stats)
			if err != nil {
				cb.error(path, err)
				errcnt += 1
				continue
			}
			if ((stats.Mode & syscall.S_IFDIR) != 0) &&
			   ((stats.Mode & syscall.S_IFLNK)==0) {
				cb.directory_attributes(path, stats)
				work_q = append(work_q, path)
				dircnt += 1
			} else {
				cb.file_attributes(path, stats)
				filecnt += 1
			}
		}
		dirfile.Close()
	}
	return filecnt, dircnt, errcnt
}

func main() {
	var args = os.Args
	if (len(args) != 2) && (len(args)!=3) {
		fmt.Printf("%v ROOT_PATH [REPEAT_COUNT]\n", args[0])
		os.Exit(1)
	}
	root_path, err := filepath.Abs(args[1])
	if err != nil {
		fmt.Printf("Invalid root path %s\n", args[1])
		os.Exit(1)
	}
	var repeat_count int
	if len(args)==3 {
		repeat_count, err = strconv.Atoi(args[2])
		if err != nil {
			fmt.Printf("Invalid repeat count: %s\n", args[2])
			os.Exit(1)
		}
	} else {
		repeat_count = 1
	}
	var callbacks = Callbacks{}
	fmt.Println("Root path: ", root_path)
	var fc, dc, ec int
	//start := time.Now()
	for i := 1; i <= repeat_count; i++ {
		fmt.Printf("Iteration %d\n", i)
		fc, dc, ec = walk(root_path, &callbacks)
	}
	//elapsed := time.Since(start)
	//elapsed_secs := float64(elapsed) / float64(time.Second)
	//rate_per_sec := float64(fc+dc)/elapsed_secs
	fmt.Printf("directories = %d, files = %d, errors = %d\n",
		dc, fc, ec)
	//fmt.Printf("Walk took %s, rate was %f files/sec = %f M files/hr.\n",
	//	elapsed, rate_per_sec, rate_per_sec*3600.0/1000000.0)
}

import java.nio.file.*;
import java.nio.file.attribute.PosixFileAttributeView;
import java.nio.file.attribute.PosixFileAttributes;
import java.util.ArrayDeque;
import java.io.IOException;


public class JavaWalker {
    // Ideally, we would just use java.nio.file.Files.walkFileTree, but it
    // does not have the correct semantics.
    public static class Callbacks {
	public void fileAttributes(Path p, PosixFileAttributes attrs) {
	    //System.out.println("File " + p.toString());
	}
        public void directoryAttributes(Path p, PosixFileAttributes attrs) {
	    //System.out.println("Directory " + p.toString());
	}
	public void error(Path p, Exception e) {
            //System.err.println("Error on path " + p.toString() + ": " + e.toString());
	    //e.printStackTrace();
	}
    }
    public static class InvalidDirectory extends Exception {
	public InvalidDirectory(Path p) {
            super("Invalid directory: " + p.toString());
	}
    }
    public static class Results {
	// It is really annoying that there isn't just a standard triple class
	public final int files;
	public final int directories;
	public final int errors;
	public Results(int files, int directories, int errors) {
	    this.files = files;
	    this.directories = directories;
	    this.errors = errors;
	}
	public String toString() {
	    return String.valueOf(directories) + " directories, " + 
		String.valueOf(files) + " files, " +
		String.valueOf(errors) + " errors";
	}
    }
    public static Results walk(Path root, Callbacks cb) throws InvalidDirectory {
	int files = 0;
	int directories = 1; // include the root
	int errors = 0;
	Path dir = root;
	PosixFileAttributes attrs;
	try {
	    attrs = Files.readAttributes(dir, PosixFileAttributes.class);
	} catch (IOException e) {
	    System.err.println("Unable to access file attributes for root");
	    throw new InvalidDirectory(dir);
	}
	if (!attrs.isDirectory()) {
	    System.err.println("Root is not a directory!");
	    throw new InvalidDirectory(dir);
	}
	cb.directoryAttributes(dir, attrs);
	ArrayDeque<Path> work_q = new ArrayDeque<Path>();
	work_q.add(dir);
	while (!work_q.isEmpty()) {
	    dir = work_q.remove();
	    // iterate through the contents of the directory
	    try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
	        for (Path file: stream) {
		    try {
			attrs = Files.readAttributes(file, PosixFileAttributes.class,
						     LinkOption.NOFOLLOW_LINKS);
		    } catch (IOException e) {
			cb.error(file, e);
			errors += 1;
			continue;
		    }
		    if (attrs.isDirectory() && !attrs.isSymbolicLink()) {
			cb.directoryAttributes(file, attrs);
			work_q.add(file);
			directories += 1;
		    }
		    else {
			cb.fileAttributes(file, attrs);
			files += 1;
		    }
		}
	    } catch (IOException e) {
		// problem in the directory stream
		cb.error(dir, e);
		errors += 1;
	    }
	}
	return new Results(files, directories, errors);
    }

    public static void main(String[] args) throws IOException {
	if (args.length!=1 && args.length!=2) {
	    System.out.println("JavaWalker ROOT_DIRECTORY [REPEAT_COUNT]");
            System.exit(1);
	}
        Path path = Paths.get(args[0]).toAbsolutePath().normalize();
        System.out.println("Walking " + path.toString());
        int repeat_count = 1;
        if (args.length==2) {
            repeat_count = Integer.parseInt(args[1]);
        }
        for (int i = 1; i <= repeat_count; i++) {
            System.out.println("Iteration " + String.valueOf(i) + "...");
            try {
		Results results = walk(path, new Callbacks());
		System.out.println("Completed walk, found " + 
				   results.toString());
	    } catch (InvalidDirectory e) {
		e.printStackTrace();
		System.exit(1);
	    }
	}
    }
}

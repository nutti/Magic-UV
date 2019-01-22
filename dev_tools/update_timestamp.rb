require 'fileutils'
require 'date'

if ARGV.size != 1 then
    puts "Usage: update_timestamp.rb <source>"
end

src_dir_path = ARGV[0].sub(/\/$/, "")
tmp_dir_path = 'tmp'

filelist = []
ignore_filelist = []
entry = Dir.glob(src_dir_path + '/**/**')
entry.each {|e|
    next e if File::ftype(e) == 'directory'
    next e if ignore_filelist.include?(e)
    filelist.push(e)
}

FileUtils.mkdir_p(tmp_dir_path) unless FileTest.exist?(tmp_dir_path)

bl_ver = nil

src_file = File.open(src_dir_path + '/__init__.py', 'r')
src_file.each_line do |line|
    if /\s*"version"\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*\,\s*(\d+)\s*\),\s*/ =~ line
        bl_ver = $1 + '.' + $2
    end
end

if bl_ver == nil
    print "Blender Version is not found"
    exit 1
end

tmp_filelist = []

filelist.each {|src_path|
    next src_path if File.extname(src_path) != '.py'

    path = src_path.dup
    path.slice!(src_dir_path)
    dest_path = tmp_dir_path + path

    # make sub directory
    idx = dest_path.rindex("/")
    sub_dir_path = dest_path[0..idx-1]
    FileUtils.mkdir_p(sub_dir_path) unless FileTest.exist?(sub_dir_path)

    # make converted file
    File.open(src_path, 'r') {|src_file|
        File.open(dest_path, 'w') {|dest_file|
            src_file.each_line do |line|
                if /^__date__/ =~ line
                    today = Date.today
                    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    line = '__date__ = "' + today.day.to_s + ' ' + mon[today.month-1] + ' ' + today.year.to_s + '"'
                end
                if /^__version__/ =~ line
                    line = '__version__ = "' + bl_ver + '"'
                end
                dest_file.puts(line)
            end
        }
    }
    tmp_filelist.push([src_path, dest_path])
}

tmp_filelist.each {|file|
    FileUtils.cp(file[1], file[0])
    puts file[0]
}


FileUtils.rm_rf(tmp_dir_path) if FileTest.exist?(tmp_dir_path)

exit 0

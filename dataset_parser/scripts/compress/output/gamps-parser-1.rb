
class Parser
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30]
    ios = true
    if ios
        FILENAME = "el-nino-gamps-cols-full-output.txt"
        PATH = "/Users/pablocerve/Documents"
        CPP = "cmake-build-debug"
    else # ubuntu
        FILENAME = "FULL-OUTPUT-PRINT-GAMPS.txt"
        PATH = "/home/pablo/Documents"
        CPP = "cmake-build-debug-ubuntu"
    end

    def initialize()
        @count = 0
        @filename = nil
        @last_filename = nil
        @last_threshold

        File.open(FILENAME, "r") do |file|
            file.each_line do |line|
                process_line(line)
            end
        end
    end


    def process_line(line)
        if line.include?("FING") and line.include?("scripts/compress")
            line.slice! "#{PATH}/FING/Proyecto/pc-tesis/cpp_project/#{CPP}/cpp_project c #{PATH}/FING/Proyecto/datasets-csv/"
            line.slice! "#{PATH}/FING/Proyecto/pc-tesis/dataset_parser/scripts/compress/output/"
            
            current_filename = line.split(" ")[1]
            if @filename == current_filename
                @count += 1
            else
                @filename = current_filename
                @last_threshold = nil
                @count = 0
            end
            @threshold = THRESHOLDS[@count].to_s

        elsif (line.include?("ratio_columns = [") and !line.include?("ratio_columns = []"))
            if @last_filename != @filename
                puts
                puts "file: " + @filename
                puts "-------------------------"
                @last_filename = @filename
            end
            if @last_threshold != @threshold
                puts
                puts @threshold + " % threshold"
                @last_threshold = @threshold
            end

            base = line.split(" ")[2]
            base.slice!(",")
            ratio = line.split("[")[1]
            puts "base: " + base + " => ratio: [" + ratio
        end
    end
end

Parser.new()

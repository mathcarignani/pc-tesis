
class Parser
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30, 50]
    ios = true
    if ios
        FILENAME = "gamps-total-no-data-and-data.txt"
        PATH = "/Users/pablocerve/Documents"
        CPP = "cmake-build-debug"
    else # ubuntu
        FILENAME = "full-output.txt"
        PATH = "/home/pablo/Documents"
        CPP = "cmake-build-debug-ubuntu"
    end

    def initialize()
        @count = 0
        @filename = nil
        @last_filename = nil
        @last_threshold = nil
        @print_sum = false
        @current_mode = nil

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
            
            current_limit_mode = line.include?("CoderGAMPSLimit") ? "GAMPSLimit" : "GAMPS"
            @current_mode = current_limit_mode
            current_filename = line.split(" ")[1] + " - " + current_limit_mode

            puts current_filename if @current_mode == "GAMPSLimit"
            if @filename == current_filename
                @count += 1
            else
                @filename = current_filename 
                @last_threshold = nil
                @count = 0
            end
            @threshold = THRESHOLDS[@count].to_s

        elsif (line.include?("ratio_columns = [") and !line.include?("ratio_columns = []"))
            # if @last_filename != @filename
            #     puts
            #     puts "file: " + @filename
            #     puts "-------------------------"
            #     @last_filename = @filename
            # end
            # if @last_threshold != @threshold
            #     puts
            #     puts @threshold + " % threshold"
            #     @print_sum = true
            #     @last_threshold = @threshold
            # end

            # base = line.split(" ")[2]
            # base.slice!(",")
            # ratio = line.split("[")[1]
            # puts "base: " + base + " => ratio: [" + ratio
        elsif line.include?("SUM") # and @print_sum
            puts line  if @current_mode == "GAMPSLimit"
            @print_sum = false  
        elsif line.include?("total_data") or line.include?("total_no_data") or line.include?("ccode group")
            puts line  if @current_mode == "GAMPSLimit"
        end
    end
end

Parser.new()
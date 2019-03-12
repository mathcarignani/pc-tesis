# run on macOS
class ColumnMaper
  COL_INDEXES = {
    "noaa-buoy" => 1,
    "noaa-adcp" => 1,
    "solar-anywhere" => 3,
    "el-nino.csv" => 7
  }
  INPUT_FILENAME = "results-gamps.txt"
  OUTPUT_FILENAME = "results-gamps-processed.txt"

  def initialize
    @output = File.open(OUTPUT_FILENAME, "w")
    File.open(INPUT_FILENAME, "r") do |file|
        file.each_line do |line|
            @output.write(line)
            process_line(line)
        end
    end
    @output.close
  end

  def process_line(line)
    if line.include?("file")
      set_dataset(line)
    elsif line.include?("base")
      print_indexes(line)
    end
  end

  def set_dataset(line)
    filename = line.split(" ")[1]
    splitted = filename.split("-")
    short_name = splitted[0] + "-" + splitted[1]
    @col_count = COL_INDEXES[short_name]
    puts "COL COUNT" + @col_count.to_s
    raise "ERROR: invalid short name: #{short_name}" unless @col_count
  end

  def print_indexes(line)
    base = line.split(" ")[1].to_i
    base_index = get_index(base)

    ratios = line.split("[")[1].split("]")[0]
    ratios = ratios.split(", ")
    ratio_indexes = []
    ratios.each do |ratio|
      ratio_indexes << get_index(ratio.to_i)
    end

    indexes_line = "base: #{base_index} => ratio: [#{ratio_indexes.join(", ")}]\n"
    @output.write(indexes_line)
  end

  def get_index(value)
    if @col_count == 1
      1
    else 
      value % @col_count
    end
  end
end

ColumnMaper.new()

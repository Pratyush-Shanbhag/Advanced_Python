import re
import collections


class Input:

    def __init__(self, data_file):
        self.data_file = data_file

    def read(self):
        raw_data = []
        file = open(self.data_file, "r")
        for line in file:
            raw_data.append(line)
        file.close()
        return raw_data


class Process:
    
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def parse_html(self, n):
        data_tuple = collections.namedtuple("data_tuple", "year value")
        data = []
        for line in self.raw_data:
            if len(re.findall(r"-?[0-9]+\.[0-9]+", line)) > n:
                data.append(data_tuple(year=re.findall(r"[0-9]{4}", line)[0], value=re.findall(r"-?[0-9]+\.[0-9]+", line)[n]))
        return data

        
class Store:

    def __init__(self):
        self.co2 = {}
        self.temp = {}
        self.database = [self.co2, self.temp]

    def store(self, co2_data, temp_data):
        for i in range(0,len(co2_data),12):
            if 1960 <= int(co2_data[i].year) <= 1990:
                self.co2[co2_data[i].year] = 0
                for val in self.generator(co2_data, i):
                    self.co2[co2_data[i].year] += float(val)
                self.co2[co2_data[i].year] /= 12
        for tupl in temp_data:
            if 1960 <= int(tupl.year) <= 1990:
                self.temp[tupl.year] = float(tupl.value)
    
    # Generator
    def generator(self, data, n):
        for j in range(n, n+12):
            yield data[n].value


class Output:

    def __init__(self, database):
        self.database = database

    def calculate_slope(self):
        sum_of_products = 0
        sum_of_co2_squared = 0
        for i in self.database[0].keys():
            sum_of_products += self.database[0][i] * self.database[1][i]
            sum_of_co2_squared += self.database[0][i]**2
        co2_values = self.database[0].values()
        temp_values = self.database[1].values()
        slope = (31*sum_of_products - sum(co2_values)*sum(temp_values)) / (31*sum_of_co2_squared - sum(co2_values)**2)
        return slope        


def main():
    co2_input = Input("./Lab_0/Co2.html")
    co2_raw_data = co2_input.read()
    co2_process = Process(co2_raw_data)
    co2_data = co2_process.parse_html(1)
    temp_input = Input("./Lab_0/Temperature.html")
    temp_raw_data = temp_input.read()
    temp_process = Process(temp_raw_data)
    temp_data = temp_process.parse_html(0)
    store = Store()
    store.store(co2_data, temp_data)
    output = Output(store.database)
    print("slope =", output.calculate_slope())


main()



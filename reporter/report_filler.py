import file_fetcher


class ReportFiller:
    fetcher = file_fetcher.FileFetcher()

    def generate(self, template_name, json_name, css_file_name, new_file_name):
        """
        Generates a report by rendering a Jinja template using data from a JSON file and a CSS file.

        Args:
            template_name (str): The name of the Jinja template file to use.
            json_name (str): The name of the JSON file to use.
            css_file_name (str): The name of the CSS file to use.
            new_file_name (str): The name of the file to save the generated report to.
        """
        template = self.fetcher.get_template(template_name)
        df = self.fetcher.get_json_data_to_dataframe(json_name)
        dictionnaire = self.get_species_data(df, json_name)
        css = self.fetcher.get_css(css_file_name)
        context = {"species_data": dictionnaire, "css_style": css}
        with open(new_file_name, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))

    def get_data(self, df, key, string=""):
        """
        Recursively extracts data from a pandas DataFrame column that matches a specified key.

        Args:
            df (pandas.DataFrame): The dataframe to extract data from.
            key (str): The key to search for in the column names.
            string (str, optional): The string to append the extracted data to. Defaults to "".

        Returns:
            str: A string representing the extracted data.
        """
        for col in df.columns:
            if key + ".content" in col:
                if isinstance(df[col][0], list):
                    for item in df[col][0]:
                        string += item + "\n\t\t\t"
                else:
                    string += df[col][0]
            if key + ".references" in col:
                if df[col][0] == []:
                    break
                else:
                    for item in df[col][0]:
                        string += "\n\t\t\t" + self.get_data(df, item)

        return string

    def get_list(self, df, key):
        """
        Extracts a list from a pandas DataFrame column that matches a specified key.

        Args:
            df (pandas.DataFrame): The dataframe to extract data from.
            key (str): The key to search for in the column names.

        Returns:
            list: A list representing the extracted data.
        """
        liste = []
        for col in df.columns:
            if key + ".content" in col:
                liste = df[col][0]
        return liste

    def get_species_data(self, df, json_name):
        """
        Extracts data from a pandas DataFrame for a specific JSON file.

        Args:
            df (pandas.DataFrame): The dataframe to extract data from.
            json_name (str): The name of the JSON file to extract data for.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        dict = {}
        liste = []
        for i in self.fetcher.get_json_data(json_name).keys():
            if i not in ["criticity_index", "current_habitats"]:
                liste.append(i)
        for item in liste:
            dict[item] = self.get_data(df, item)
        dict["current_habitats"] = self.get_list(df, "current_habitats")
        return dict

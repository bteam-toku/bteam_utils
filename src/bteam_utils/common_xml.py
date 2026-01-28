import xml.etree.ElementTree as Et
from xml.dom import minidom

class CommonXML:
    def __init__(self) -> None:
        """コンストラクタ
        """
        pass
    
    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    def pretty_tree(self, element:Et.Element) -> None:
        """XMLデータの整形

        Args:
            element : rootのElement
        """
        xml_string = minidom.parseString(Et.tostring(element, 'utf-8'))
        return(xml_string.toprettyxml())

    def save_xml(self, element:Et.Element, outfile_path:str) -> None:
        """XMLファイルの保存

        Args:
            element (Et.Element): rootのElement
            outfile_path (str): 保存ファイル名
        """
        xml_string = self.pretty_tree(element)
        with open(outfile_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)

    def save_csv(self, element:Et.Element, outfile_path:str, key_header:str, key_body:str) -> None:
        """XMLをCSVに変換

        Args:
            element (Et.Element): rootのElement
            key_header (str): Header部のname
            key_body (str): Body部のname
        """
        # Parse xml file
        root = element

        # Create csv file
        with open(outfile_path, "w", encoding='utf-8-sig', newline='') as fout:
            # Write header
            header = root.find(key_header)
            fout.write(','.join(element.attrib["name"] for element in header) + '\n')
            tags = [element.tag for element in header]

            # Write tickets
            tickets = root.findall(key_body)
            for ticket in tickets:
                row_data = []
                for tag in tags:
                    el = ticket.find(tag)
                    el_text = el.text if el is not None else None

                    if el_text is None or str(el_text) == "None":
                        row_data.append('')
                    else:
                        row_data.append(f'"{str(el_text).replace('"', '""')}"')
                fout.write(','.join(row_data) + '\n')

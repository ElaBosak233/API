class HtmlParser:
    HTML = ""
    Bulleted_List_Counter = 0

    def __init__(self, source):
        global text
        for item in source["results"]:
            item_type = item["type"]
            if item_type == "heading_1":
                text = item[item_type]["rich_text"]
                for i in text:
                    self.heading_1(i)
            elif item_type == "heading_2":
                text = item[item_type]["rich_text"]
                for i in text:
                    self.heading_2(i)
            elif item_type == "heading_3":
                text = item[item_type]["rich_text"]
                for i in text:
                    self.heading_3(i)
            elif item_type == "paragraph":
                text = item[item_type]["rich_text"]
                self.HTML += "<div>"
                for i in text:
                    self.paragraph(i)
                self.HTML += "</div>"
            elif item_type == "bulleted_list_item":
                if self.Bulleted_List_Counter == 0:
                    self.HTML += "<ul>"
                text = item[item_type]["rich_text"]
                self.Bulleted_List_Counter += 1
                self.HTML += "<li>"
                for i in text:
                    self.div_inline(i)
                self.HTML += "</li>"
            elif item_type == "image":
                if "external" in item[item_type]:
                    self.img(item[item_type]["external"]["url"])
                elif "file" in item[item_type]:
                    self.img(item[item_type]["file"]["url"])
            elif item_type == "toggle":
                from api.notion.main import notion
                cd = notion.blocks.children.list(block_id=item["id"])
                r = HtmlParser(cd).export()
                self.HTML += "<details>"
                self.HTML += "<summary>"
                text = item[item_type]["rich_text"]
                for i in text:
                    self.div_inline(i)
                self.HTML += "</summary>"
                self.HTML += r
                self.HTML += "</details>"
            if self.Bulleted_List_Counter != 0 and item_type != "bulleted_list_item":
                self.Bulleted_List_Counter = 0
                self.HTML += "</ul>"

    def export(self):
        return self.HTML

    @staticmethod
    def get_style(annotations):
        style = ""
        if annotations["bold"]:
            style += 'font-weight: bold;'
        if annotations["italic"]:
            style += 'font-style: italic;'
        if annotations["underline"]:
            style += 'text-decoration: underline;'
        if annotations["color"]:
            style += f'color: {annotations["color"]};'
        # TODO 其他样式省略
        return style

    def div_inline(self, ctx):
        r = f"""
        <div style="display: inline; {self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</div>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def paragraph(self, ctx):
        r = f"""
        <p style="display: inline; {self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</p>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def text(self, ctx):
        r = f"""
        <span style="display: inline; {self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</span>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def heading_1(self, ctx):
        r = f"""
        <h1 style="{self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</h1>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def heading_2(self, ctx):
        r = f"""
        <h2 style="{self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</h2>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def heading_3(self, ctx):
        r = f"""
        <h3 style="{self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</h3>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def bulleted_list_item(self, ctx):
        r = f"""
        <li style="{self.get_style(ctx["annotations"])}">{ctx["text"]["content"]}</li>
        """
        if ctx["href"]:
            r = f"""<a href={ctx["href"]}>{r}</a>"""
        self.HTML += r

    def img(self, ctx):
        r = f"""
        <img src={ctx} />
        """
        self.HTML += r

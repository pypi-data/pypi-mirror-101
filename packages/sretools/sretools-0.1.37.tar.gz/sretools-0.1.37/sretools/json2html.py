#!/usr/bin/env python3
# Yonghang Wang

import sys
import argparse
import os
import re
import json
import yaml


class JsonConverter:
    def __init__(
        self,
        jsstr,
        tblattr="border-collapse:collapse;",
        sort=False,
        sort_by_val=False,
        sortkeywords=None,
        recursive=False,
        keys_included=None,
        keys_excluded=None,
        colors=None,
    ):
        if type(jsstr) is list or type(jsstr) is dict:
            self.__obj = jsstr
        else:
            try:
                self.__obj = json.loads(jsstr)
            except:
                print("# not invalid JSON.")
                sys.exit(0)
        if type(self.__obj) is dict:
            if keys_included:
                self.__obj = {k: v for k, v in self.__obj.items() if k in keys_included}
            if keys_excluded:
                for keys in keys_excluded:
                    klst = re.split(r"\.", keys)
                    pt = self.__obj
                    good = True
                    for k in klst[:-1]:
                        if k not in pt:
                            print(
                                "# warning. ignored invalid key series: {}".format(keys)
                            )
                            good = False
                            break
                        pt = pt[k]
                    if good:
                        del pt[klst[-1]]
        self.__recursive = recursive
        self.__sort = sort
        self.__sort_by_val = sort_by_val
        self.__tblattr = tblattr
        self.__sortkeywords = sortkeywords
        if colors:
            self.__colors = re.split(",", colors)
        else:
            self.__colors = None
        self.__lastcolor = 0

    def json2html(self):
        return self.json2html_helper(self.__obj)

    def __is_final_list(self, lst):
        if not type(lst) is list:
            return False
        for r in lst:
            if type(r) is dict or type(r) is list:
                return False
        return True

    def __is_final_tbl(self, lst):
        if not type(lst) is list:
            return False
        for r in lst:
            if not self.__is_final_dt(r):
                return False
        return True

    def __is_final_dt(self, dt):
        if not type(dt) is dict:
            return False
        for k, v in dt.items():
            if type(v) is dict or type(v) is list:
                return False
        return True

    def json2yaml(self):
        return yaml.safe_dump(self.__obj, default_flow_style=False)

    def json2html_helper(self, obj):
        out = ""
        inlist_border = 1
        if type(obj) is not list and type(obj) is not dict:
            if self.__recursive:
                try:
                    o = json.loads(obj)
                    out += self.json2html_helper(o)
                except:
                    out += str(obj)
            else:
                out += str(obj)
            return out
        if self.__colors:
            c = self.__colors[self.__lastcolor]
            self.__lastcolor = (self.__lastcolor + 1) % len(self.__colors)
            colstr = "background-color:{}".format(c)
        else:
            colstr = ""
        if type(obj) is list:
            if self.__sort:
                obj = sorted(obj)
            style = 'style="{};{}"'.format(self.__tblattr, colstr)
            if self.__is_final_list(obj):
                for r in obj:
                    r = str(r).replace("\r\n", "<br>")
                    r = str(r).replace("\n", "<br>")
                    out += "<li>" + str(r) + "</li>\n"
            elif self.__is_final_tbl(obj):
                out += "<table {} border={}>\n".format(style, inlist_border)
                need_switch = len(obj) > 1
                colors = ["#FFFFFF", "#EEFFEB"]
                ix = 0
                for r in obj:
                    c = colors[ix]
                    ix = 1 - ix
                    for k, v in r.items():
                        if not v:
                            v = ""
                        else:
                            v = str(v).replace("\r\n", "<br>")
                            v = str(v).replace("\n", "<br>")
                        if need_switch:
                            out += '<tr style="background-color:{}">\n'.format(c)
                        else:
                            out += "<tr>\n"
                        out += "<td><b>" + str(k) + "</b></td>\n"
                        out += "<td>" + str(v) + "</td>\n"
                        out += "</tr>\n"
                    # + sepbar
                    # out += "<tr><td></td><td></td></tr>\n"
                out += "</table>\n"
            else:
                out += "<table {} border={}>\n".format(style, inlist_border)
                for o in obj:
                    out += "<tr>\n"
                    out += "<td>\n"
                    out += self.json2html_helper(o)
                    out += "</td>\n"
                    out += "</tr>\n"
                out += "</table>\n"
            return out
        if type(obj) is dict:
            if self.__sort:
                if self.__sort_by_val:
                    fs = lambda t: t[1]
                else:
                    fs = lambda t: t[0]
            else:
                fs = lambda t: t
            if self.__sortkeywords:

                def f(s):
                    stbl = {
                        s: ix
                        for ix, s in enumerate(re.split(r",", self.__sortkeywords))
                    }
                    return (stbl.get(s, 999999), s)

                fs = lambda t: f(t[0])
            style = 'style="{};{}"'.format(self.__tblattr, colstr)
            out += "<table {} border={}>\n".format(style, inlist_border)
            for k, v in sorted(obj.items(), key=fs):
                out += "<tr>\n"
                out += "<td><b>" + str(k) + "</b></td>\n"
                out += "<td>\n"
                out += self.json2html_helper(v)
                out += "</td>\n"
                out += "</tr>\n"
            out += "</table>\n"
            return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--infile", dest="infile", help="input file")
    parser.add_argument(
        "-a",
        "--table_attributes",
        dest="attributes",
        default="border-collapse:collapse;",
        help="table attributes",
    )
    parser.add_argument(
        "-s",
        "--sorted",
        dest="sorted",
        action="store_true",
        default=False,
        help="try best to make sure output is sorted. default by key.",
    )
    parser.add_argument(
        "-C", "--colors", dest="colors", help="background colors to be used."
    )
    parser.add_argument(
        "-k",
        "--keywords_order",
        dest="keyorder",
        help="use this ordered keywords to help sort dict.",
    )
    parser.add_argument(
        "-I",
        "--keys-included",
        dest="keys_included",
        action="append",
        help="include these TOP level keys only",
    )
    parser.add_argument(
        "-E",
        "--keys-excluded",
        dest="keys_excluded",
        action="append",
        help="exclude these keys. eg. k1 or k2.k3",
    )
    parser.add_argument(
        "-v",
        "--dictsortbyvalue",
        dest="dtbyval",
        action="store_true",
        default=False,
        help="with -s, sort dict by value.",
    )
    parser.add_argument(
        "-Y",
        "--yaml",
        dest="yaml",
        action="store_true",
        default=False,
        help="dump in YAML format",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        default=False,
        help="if str value is JSON, treat it as JSON object ",
    )
    parser.add_argument(
        "-X",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="debug mode",
    )
    args = parser.parse_args()

    if args.infile:
        if not os.path.isfile(args.infile):
            print("{} not exists.")
        with open(args.infile, "r") as f:
            INPUT = f.read()
    else:
        INPUT = sys.stdin.read()

    if args.yaml:
        print(
            JsonConverter(
                INPUT,
                tblattr=args.attributes,
                sort=args.sorted,
                sort_by_val=args.dtbyval,
                keys_included=args.keys_included,
                keys_excluded=args.keys_excluded,
                sortkeywords=args.keyorder,
            ).json2yaml()
        )
        sys.exit(0)

    print(
        JsonConverter(
            INPUT,
            tblattr=args.attributes,
            sort=args.sorted,
            sort_by_val=args.dtbyval,
            sortkeywords=args.keyorder,
            recursive=args.recursive,
            keys_included=args.keys_included,
            keys_excluded=args.keys_excluded,
            colors=args.colors,
        ).json2html()
    )


if __name__ == "__main__":
    main()

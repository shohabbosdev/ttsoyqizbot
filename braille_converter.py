class BrailleConverter:
    class Chars:
        chars    = "abdefghijklmnopqrstuvxyz"
        db_chars = ["o'", "g'","sh","ch"]
        numbers  = "1234567890"
        symbols  = ",;:.?!\"()…-" # [7, 8, 9] "()…" - is functionality

    class Braille:
        chars    = "⠁⠃⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠽⠗⠎⠞⠥⠺⠹⠯⠵"
        db_chars = "⠧⠻⠱⠟"
        numbers  = "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚"
        symbols  = "⠂⠆⠒⠲⠢⠖⠴⠶⠶⠄⠤"
        specific = "⠨⠼⠸⠀" # Capital, numeric, italic, space

    class Binary:
        chars = [
            32, 48, 38, 34, 52, 54, 50, 20,
            22, 40, 56, 44, 46, 42, 60, 47,
            58, 28, 30, 41, 23, 39, 61, 43
        ]

        db_chars = [57, 55, 35, 62]
        numbers = [32, 48, 36, 38, 34, 52, 54, 50, 20, 22]
        symbols = [16, 24, 18, 19, 17, 26, 11, 27, 8, 9]
        specific = [5, 15, 7, 0]

    def decimal_to_int(self, s):
        return sum(2**(6-int(i)) for i in s)

    def int_to_decimal(self, n):
        shifr = bin(n)[2:].zfill(6)

        s=""
        for i in range(len(shifr)):
            if shifr[i]=="1":
                s+=str(i+1)

        return s


    def convert_braille_to_chars(self, s):
        ans = ""

        dots = 0

        scoped    = False
        isCapital = False
        isNum     = False
        isItalic  = False

        for i in s:
            if i!=self.Braille.symbols[9]:
                dots=0

            if i==self.Braille.specific[3]:
                ans += " "
                isNum = False
                continue

            if i in self.Braille.specific:
                ind = self.Braille.specific.index(i)

                if ind==0: isCapital = True
                if ind==1: isNum     = True
                if ind==2: isItalic  = True
                continue

            if isNum and i in self.Braille.numbers:
                ind = self.Braille.numbers.index(i)
                ans += self.Chars.numbers[ind]
                continue

            if i in self.Braille.symbols:
                ind = self.Braille.symbols.index(i)

                ch = self.Chars.symbols[ind]
                if ind==7: # ⠶⠶ ()
                    if scoped:
                        ch = self.Chars.symbols[ind+1]
                        scoped = False
                    else:
                        scoped = True
                if ind==9: # ⠄… 
                    dots+=1

                    if dots!=3:
                        continue

                ans += ch
                continue

            if i in self.Braille.db_chars:
                ind = self.Braille.db_chars.index(i)
                ch = self.Chars.db_chars[ind]

                if isCapital:
                    ans += ch.title()
                    isCapital = False
                else:
                    ans += ch

                continue

            if i in self.Braille.chars:
                ind = self.Braille.chars.index(i)
                ch = self.Chars.chars[ind]

                if isCapital:
                    ans += ch.title()
                    isCapital = False
                else:
                    ans += ch

            continue

        return ans

    def convert_chars_to_braille(self, s):
        size = len(s)

        ans = ""
        isNum = False

        i=0
        while i<size:
            cur = s[i].lower()

            if s[i]==" ":
                ans += self.Braille.specific[3]
                isNum = False

                i+=1
                continue

            if s[i] in self.Chars.symbols:
                ind = self.Chars.symbols.index(cur)

                if ind==9: # … ⠄⠄⠄
                    ans += self.Braille.symbols[ind]*2

                ans += self.Braille.symbols[ind]

                i+=1
                continue

            if s[i] in self.Chars.numbers:
                ind = self.Chars.numbers.index(cur)

                if not isNum:
                    ans += self.Braille.specific[1]
                    isNum = True
                
                ans += self.Braille.numbers[ind]

                i+=1
                continue

            if i+1<size:
                db_cur = s[i]+s[i+1]
                low = db_cur.lower()

                if low in self.Chars.db_chars:
                    ind = self.Chars.db_chars.index(low)

                    if low!=db_cur:
                        ans += self.Braille.specific[0]

                    ans += self.Braille.db_chars[ind]

                    i+=2
                    continue

            if cur in self.Chars.chars:
                ind = self.Chars.chars.index(cur)

                ch = self.Braille.chars[ind]

                if s[i]!=cur:
                    ans += self.Braille.specific[0]

                ans += ch

                i+=1
                continue

            i+=1

        return ans

    def convert_braille_to_binary(self, s):
        a = []
        for i in s:
            k = bin(ord(i)-10240)[2:]
            z = k.zfill(6)[::-1]
            m = list(map(int,list(z)))
            a += [m]

        return a

    def convert_braille_to_digits(self, s):
        s = self.convert_braille_to_binary(s)
        a = []
        for i in s:
            v = ""
            for j in range(len(i)):
                if i[j]:
                    v += str(j+1)
            a+=[v]
        
        return a

    def convert_char_to_binary(self, s):
        braille = self.convert_chars_to_braille(s)
        binar   = self.convert_braille_to_binary(braille)

        return binar

    def viewer(self, s, t="binar"):
        ans=[]
        if t == "binar":
            for i in s:
                ans += [
                    f"{i[0]}{i[3]}\n{i[1]}{i[4]}\n{i[2]}{i[5]}\n\n"
                ]
        
        return ans


if __name__ == "__main__":
    converter = BrailleConverter()

    def test(s):
        input_text = s

        braille = converter.convert_chars_to_braille(input_text)
        text    = converter.convert_braille_to_chars(braille)
        binar   = converter.convert_braille_to_binary(braille)
        digits  = converter.convert_braille_to_digits(braille)

        print(*converter.viewer(binar), sep="")

        print(input_text)
        print(braille)
        print(text)
        print(binar)
        print(input_text==text)
        print(digits)
        print()
    
    test("Assalomu alaykum do'stlar, qalaysizlar meni nomerim 998941956231")
    test("jo'ja g'isht shift ombor (ichidagi) odam")

"""
10240 ⠀   |10241 ⠁ a |10242 ⠂ , |10243 ⠃ b |
10244 ⠄   |10245 ⠅ k |10246 ⠆ ; |10247 ⠇ l |
10248 ⠈   |10249 ⠉   |10250 ⠊ i |10251 ⠋ f |
10252 ⠌   |10253 ⠍ m |10254 ⠎ s |10255 ⠏ p |
10256 ⠐   |10257 ⠑ e |10258 ⠒ : |10259 ⠓ h |
10260 ⠔   |10261 ⠕ o |10262 ⠖ ! |10263 ⠗ r |
10264 ⠘   |10265 ⠙ d |10266 ⠚ j |10267 ⠛ g |
10268 ⠜   |10269 ⠝ n |10270 ⠞ t |10271 ⠟ ch|
10272 ⠠   |10273 ⠡   |10274 ⠢ ? |10275 ⠣   |
10276 ⠤ - |10277 ⠥ u |10278 ⠦   |10279 ⠧ o'|
10280 ⠨   |10281 ⠩   |10282 ⠪   |10283 ⠫   |
10284 ⠬   |10285 ⠭   |10286 ⠮   |10287 ⠯ y |
10288 ⠰   |10289 ⠱ sh|10290 ⠲ . |10291 ⠳   |
10292 ⠴ " |10293 ⠵ z |10294 ⠶   |10295 ⠷   |
10296 ⠸   |10297 ⠹ x |10298 ⠺ v |10299 ⠻ g'|
10300 ⠼   |10301 ⠽ q |10302 ⠾   |10303 ⠿   |
"""
class PrintUtils:
    @classmethod
    def percentage(cls, part, whole, numbers_after_comma=2):
        return round(100 * float(part)/float(whole), numbers_after_comma)
from django.db import models

# Create your models here.
class Event(models.Model):
    発生日 = models.DateField(verbose_name="発生日")
    発生時間 = models.TimeField(verbose_name="発生時間")
    発生場所 = models.CharField(max_length=255, verbose_name="発生場所")
    事件名 = models.CharField(max_length=255, verbose_name="事件名")
    事件の概要 = models.TextField(verbose_name="事件の概要")
    # 以下、被疑者、被害者、関係者のモデルフィールドは、簡単のため文字列フィールドとしていますが、
    # 実際にはより複雑な関係やモデル設計が必要になる可能性があります。
    被疑者の人定事項 = models.CharField(max_length=255, verbose_name="被疑者の人定事項", blank=True)
    被害者の人定事項 = models.CharField(max_length=255, verbose_name="被害者の人定事項", blank=True)
    関係者の人定事項 = models.CharField(max_length=255, verbose_name="関係者の人定事項", blank=True)

    def __str__(self):
        return self.事件名
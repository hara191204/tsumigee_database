from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

# フリガナ用バリデータ：全角カタカナ・長音符・半角数字のみ許可
FURIGANA_VALIDATOR = RegexValidator(
    regex=r"^[ァ-ヶー0-9]+$",
    message="フリガナは全角カタカナ、長音符（ー）、半角数字のみ使用できます。",
)


class Maker(models.Model):
    """ゲームメーカーのマスタテーブル"""

    name = models.CharField(
        verbose_name="名前",
        max_length=255,
    )

    furigana = models.CharField(
        verbose_name="フリガナ",
        max_length=255,
        validators=[FURIGANA_VALIDATOR],
    )

    is_bishojo_brand = models.BooleanField(
        verbose_name="美少女ゲームブランド",
        default=False,
    )

    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー"
        ordering = ["furigana"]

    def __str__(self):
        return self.name


class Hard(models.Model):
    """ゲームハードのマスタテーブル（PS5, Switch, PC, FC等）"""

    name = models.CharField(
        verbose_name="名前",
        max_length=32,
    )

    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "ハード"
        verbose_name_plural = "ハード"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Game(models.Model):
    """所持ゲームソフトの管理テーブル"""

    class ClearStatusChoices(models.TextChoices):
        CLEAR = "clear", "クリア"
        TSUMI = "tsumi", "積み"
        COLLECTION_ONLY = "collection_only", "コレクションのみ"

    class GradeChoices(models.TextChoices):
        SPLUS = "S+", "S+"
        S = "S", "S"
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        NA = "-", "-"

    title = models.CharField(
        verbose_name="タイトル",
        max_length=255,
    )

    furigana = models.CharField(
        verbose_name="フリガナ",
        max_length=255,
        validators=[FURIGANA_VALIDATOR],
    )

    maker = models.ForeignKey(
        Maker,
        verbose_name="メーカー",
        on_delete=models.PROTECT,
        related_name="games",
    )

    hard = models.ForeignKey(
        Hard,
        verbose_name="ハード",
        on_delete=models.PROTECT,
        related_name="original_games",
    )

    # 実際にプレイ可能なハード（任意項目）
    # 例: アイスクライマーをWiiのバーチャルコンソールで所持している場合
    #     hard = FC, playable_games = Wii となる
    play_hard = models.ForeignKey(
        Hard,
        verbose_name="プレイ可能ハード",
        on_delete=models.SET_NULL,
        related_name="playable_games",
        null=True,
        blank=True,
    )

    clear_status = models.CharField(
        verbose_name="クリア状況",
        max_length=15,
        choices=ClearStatusChoices.choices,
        default=ClearStatusChoices.TSUMI,
    )

    grade = models.CharField(
        verbose_name="評価",
        max_length=4,
        choices=GradeChoices.choices,
        default=GradeChoices.NA,
    )

    is_package = models.BooleanField(
        verbose_name="パッケージ所有",
        default=False,
    )

    is_bishojo = models.BooleanField(
        verbose_name="美少女ゲーム",
        default=False,
    )

    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
    )

    # clear_statusが「積み」から「クリア」に変わったタイミングで記録する。
    # 自動更新ではないため、保存処理側（save()のオーバーライドやフォーム側）で
    # 明示的にセットする実装が別途必要
    cleared_at = models.DateTimeField(
        verbose_name="クリア日時",
        null=True,
        blank=True,
    )

    note = models.TextField(
        verbose_name="備考",
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "ゲーム"
        verbose_name_plural = "ゲーム"
        ordering = ["furigana"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tsumigee_database:game_list")

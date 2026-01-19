"""create examination_tickets and seed data

Revision ID: 20250218_01
Revises: 
Create Date: 2025-02-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20250218_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "examination_tickets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("number", sa.Integer(), nullable=False, unique=True),
        sa.Column("description_first_task", sa.Text(), nullable=False),
    )

    tickets_table = sa.table(
        "examination_tickets",
        sa.column("number", sa.Integer()),
        sa.column("description_first_task", sa.Text()),
    )

    op.bulk_insert(
        tickets_table,
        [
            {
                "number": 1,
                "description_first_task": "Понятие числового ряда. Сходимость и расходимость рядов",
            },
            {
                "number": 2,
                "description_first_task": "Признаки сходимости рядов с неотрицательными членами. Теоремы сравнения",
            },
            {
                "number": 3,
                "description_first_task": "Признаки Коши, Даламбера, интегральный признак",
            },
            {
                "number": 4,
                "description_first_task": "Ряды с членами произвольного знака. Признак Лейбница",
            },
            {
                "number": 5,
                "description_first_task": "Абсолютная и условная сходимость числовых рядов",
            },
            {
                "number": 6,
                "description_first_task": "Область сходимости функционального ряда",
            },
            {
                "number": 7,
                "description_first_task": "Степенные ряды. Область сходимости",
            },
            {
                "number": 8,
                "description_first_task": "Тригонометрические ряды Фурье для функций с периодом 2π",
            },
            {
                "number": 9,
                "description_first_task": "Тригонометрические ряды Фурье для функций с произвольным периодом",
            },
            {
                "number": 10,
                "description_first_task": "Разложение функций в ряд Фурье. Вычисление коэффициентов ряда Фурье",
            },
            {
                "number": 11,
                "description_first_task": "Определения показательной и тригонометрических функций комплексного переменного",
            },
            {
                "number": 12,
                "description_first_task": "Определения гиперболических функций и их связь с тригонометрическими функциями",
            },
            {
                "number": 13,
                "description_first_task": "Логарифмическая функция комплексного переменного",
            },
            {
                "number": 14,
                "description_first_task": "Производная функции комплексного переменного. Условия Коши-Римана",
            },
            {
                "number": 15,
                "description_first_task": "Определение и вычисление интеграла от функции комплексного переменного",
            },
            {
                "number": 16,
                "description_first_task": "Интегральная формула Коши",
            },
            {
                "number": 17,
                "description_first_task": "Производные высших порядков аналитической функции",
            },
            {
                "number": 18,
                "description_first_task": "Разложение аналитической функции в ряд Тейлора",
            },
            {
                "number": 19,
                "description_first_task": "Разложение функции в ряд Лорана",
            },
            {
                "number": 20,
                "description_first_task": "Классификация изолированных особых точек",
            },
            {
                "number": 21,
                "description_first_task": "Определение вычета функции",
            },
            {
                "number": 22,
                "description_first_task": "Нахождение вычетов в устранимых и существенно особых точках",
            },
            {
                "number": 23,
                "description_first_task": "Нахождение вычетов в полюсах",
            },
            {
                "number": 24,
                "description_first_task": "Основная теорема о вычетах",
            },
            {
                "number": 25,
                "description_first_task": "Преобразование Лапласа. Оригиналы, изображения и их свойства",
            },
            {
                "number": 26,
                "description_first_task": "Изображения элементарных функций",
            },
            {
                "number": 27,
                "description_first_task": "Теорема смещения и линейность изображения",
            },
            {
                "number": 28,
                "description_first_task": "Дифференцирование и интегрирование оригинала",
            },
            {
                "number": 29,
                "description_first_task": "Дифференцирование и интегрирование изображения",
            },
            {
                "number": 30,
                "description_first_task": "Применение теорем операционного исчисления к решению дифференциальных уравнений",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("examination_tickets")

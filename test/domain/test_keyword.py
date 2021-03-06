from unittest import TestCase

from underlines.domain import underline, book, keyword

target = """인간의 왕조가 흥망성쇠를 거듭하는 동안 이 작은 씨앗은 미래에 대한 희망을 버리지 않고 고집스럽게 버틴 것이다.    
                    그러다가 어느 날 그 작은 식물의 열망이 어느 실험실 안에서 활짝 피었다. 그 연꽃은 지금 어디 있을까. 모든 시작은 기다림의 끝이다.
                    우리는 모두 단 한 번의 기회를 만난다. 우리는 모두 한 사람 한 사람 불가능하면서도 필연적인 존재들이다. 
                    모든 우거진 나무의 시작은 기다림을 포기하지 않은 씨앗이었다."""

class TestKeyword(TestCase):

    def test_analize_entities(self):
        keywords = keyword.find_keyword(target, 2)
        assert len(keywords) == 2
        assert type(keywords[0]) is str

    def test_save(self):
        ## Init
        keyword.init_table()
        underline.init_table()
        book.init_table()
        ## Given
        found = book.find_by_isbn13("9791160560367")
        book.save(found)
        underline_id = underline.save("9791160560367", "underline")
        ## When
        keyword_id= keyword.save(underline_id, "키워드")
        ## Then
        saved = keyword.get_by_isbn13("9791160560367")
        assert saved[0]['keyword'] == "키워드"

    def test_remove_duplicated_name(self):
        dummy_entities= [make_dummy_entity("키워드1", 0.6), make_dummy_entity("키워드1", 0.6), make_dummy_entity("키워드2", 0.6), make_dummy_entity("키워드3", 0.6)]
        unique_entities = keyword._remove_duplicated_name(dummy_entities)
        assert unique_entities[0].name == "키워드1"
        assert unique_entities[1].name == "키워드2"

class DummyEntity(object):
    name = ""
    salience = ""

    def __init__(self, name, salience):
        self.name = name
        self.salience = salience

def make_dummy_entity(name, salience):
    entity = DummyEntity(name, salience)
    return entity
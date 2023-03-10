from .base import Model
from .utils import get_fields_data, set_quote

class User(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'sj_id', 'nickname', 
            'pw', 'name', 'major', 
            'is_admin', 'sejong_auth', 
            'created_at', 'updated_at', 'version']

    def insert_user(self, user_data:dict):
        keys, values = get_fields_data(user_data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote, values)))
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def get_user_by_single_property(self, property, input_property):
        """한 속성에 해당하는 속성값을 통해 사용자를 찾는다"""
        query = self.select_query.format(
            property="*",
            table_name=self.table_name,
            condition=f"WHERE {property}={set_quote(input_property)}"
        )
        self.cursor.execute(query)
        user_data = self.cursor.fetchone()
        self.cursor.close()
        if user_data is None:
            return None
        else:
            return dict(zip(self.property, user_data))
    
    def delete_user_by_id(self, id:str):
        """id에 해당하는 사용자를 삭제한다."""
        query = self.delete_query.format(
            table_name=self.table_name,
            condition=f'WHERE id="{id}"'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()


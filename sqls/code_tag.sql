CREATE TABLE CODE_BOOK.CODE_TAGS (
	id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
	tag_name VARCHAR2(100) NOT NULL UNIQUE
);
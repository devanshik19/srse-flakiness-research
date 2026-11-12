package com.j256.ormlite.table;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.sql.SQLException;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.j256.ormlite.BaseCoreTest;
import com.j256.ormlite.field.DatabaseField;

public class SchemaUtils_dropSchema_0_0_Test extends BaseCoreTest {

	private final static String SCHEMA_NAME = "dropschematest0";

	@Override
	@BeforeEach
	public void before() throws Exception {
		super.before();
	}

	@Test
	public void testDropExistingSchema() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, true);
		assertTrue(SchemaUtils.createSchema(connectionSource, DropSchemaEntity.class) > 0);
		assertEquals(1, SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, false));
	}

	@Test
	public void testDropMissingSchemaIgnoreErrors() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, true);
		assertEquals(1, SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, true));
	}

	@Test
	public void testDropMissingSchemaThrows() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, true);
		assertThrows(SQLException.class,
				() -> SchemaUtils.dropSchema(connectionSource, DropSchemaEntity.class, false));
	}

	@Test
	public void testPrivateConstructor() throws Exception {
		java.lang.reflect.Constructor<SchemaUtils> c = SchemaUtils.class.getDeclaredConstructor();
		c.setAccessible(true);
		c.newInstance();
	}

	@DatabaseTable(tableName = "droptable", schemaName = SCHEMA_NAME)
	protected static class DropSchemaEntity {
		@DatabaseField(generatedId = true)
		public int id;
		@DatabaseField
		public int val;

		public DropSchemaEntity() {
		}
	}
}

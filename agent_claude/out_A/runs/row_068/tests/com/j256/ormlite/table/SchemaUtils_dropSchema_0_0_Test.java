package com.j256.ormlite.table;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.sql.SQLException;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.j256.ormlite.BaseCoreTest;
import com.j256.ormlite.field.DatabaseField;

public class SchemaUtils_dropSchema_0_0_Test extends BaseCoreTest {

	private final static String SCHEMA_NAME = "dropschema00";

	@Override
	@BeforeEach
	public void before() throws Exception {
		super.before();
	}

	@Test
	public void testDropExistingSchema() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, true);
		assertTrue(SchemaUtils.createSchema(connectionSource, SchemaEntity.class) > 0);
		assertEquals(1, SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, false));
	}

	@Test
	public void testDropMissingSchemaIgnoreErrors() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, true);
		assertEquals(1, SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, true));
	}

	@Test
	public void testDropMissingSchemaThrows() throws SQLException {
		SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, true);
		assertThrows(SQLException.class, () -> SchemaUtils.dropSchema(connectionSource, SchemaEntity.class, false));
	}

	@Test
	public void testPrivateConstructor() throws Exception {
		Constructor<SchemaUtils> c = SchemaUtils.class.getDeclaredConstructor();
		assertTrue(Modifier.isPrivate(c.getModifiers()));
		c.setAccessible(true);
		c.newInstance();
	}

	@DatabaseTable(tableName = "tbl", schemaName = SCHEMA_NAME)
	protected static class SchemaEntity {
		@DatabaseField(generatedId = true)
		public int id;
		@DatabaseField
		public int val;

		public SchemaEntity() {
		}
	}
}

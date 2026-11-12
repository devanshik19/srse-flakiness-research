package com.j256.ormlite.table;

import static org.easymock.EasyMock.*;
import static org.junit.jupiter.api.Assertions.*;

import java.sql.SQLException;
import java.util.List;
import java.util.ArrayList;

import org.easymock.IAnswer;
import org.junit.jupiter.api.Test;

import com.j256.ormlite.db.DatabaseType;
import com.j256.ormlite.field.FieldType;
import com.j256.ormlite.stmt.StatementBuilder.StatementType;
import com.j256.ormlite.support.CompiledStatement;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;

public class SchemaUtils_createSchema_0_0_Test {

	private DatabaseType dbType(boolean neg, boolean zero) {
		DatabaseType dt = createNiceMock(DatabaseType.class);
		expect(dt.isCreateSchemaReturnsNegative()).andReturn(neg).anyTimes();
		expect(dt.isCreateSchemaReturnsZero()).andReturn(zero).anyTimes();
		dt.appendEscapedEntityName(anyObject(StringBuilder.class), anyObject(String.class));
		expectLastCall().andAnswer(new IAnswer<Object>() {
			@Override
			public Object answer() {
				Object[] args = getCurrentArguments();
				((StringBuilder) args[0]).append('"').append(args[1]).append('"');
				return null;
			}
		}).anyTimes();
		replay(dt);
		return dt;
	}

	private Object[] setup(DatabaseType dt) throws Exception {
		ConnectionSource cs = createMock(ConnectionSource.class);
		DatabaseConnection conn = createMock(DatabaseConnection.class);
		CompiledStatement stmt = createMock(CompiledStatement.class);
		expect(cs.getDatabaseType()).andReturn(dt).anyTimes();
		expect(cs.getReadWriteConnection("schema")).andReturn(conn);
		cs.releaseConnection(conn);
		expectLastCall();
		return new Object[] { cs, conn, stmt };
	}

	@Test
	public void testSuccess() throws Exception {
		DatabaseType dt = dbType(false, false);
		Object[] o = setup(dt);
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(eq("CREATE SCHEMA \"schema\""), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(0);
		stmt.close();
		expectLastCall();
		replay(cs, conn, stmt);
		assertEquals(1, SchemaUtils.createSchema(cs, "schema"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testPositiveRowsNotExpectingZero() throws Exception {
		Object[] o = setup(dbType(false, false));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(3);
		stmt.close();
		replay(cs, conn, stmt);
		assertEquals(1, SchemaUtils.createSchema(cs, "schema"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testPositiveRowsExpectingZero() throws Exception {
		Object[] o = setup(dbType(false, true));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(3);
		stmt.close();
		replay(cs, conn, stmt);
		assertThrows(SQLException.class, () -> SchemaUtils.createSchema(cs, "schema"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testNegativeRowsNotAllowed() throws Exception {
		Object[] o = setup(dbType(false, false));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(-1);
		stmt.close();
		replay(cs, conn, stmt);
		SQLException e = assertThrows(SQLException.class, () -> SchemaUtils.createSchema(cs, "schema"));
		assertTrue(e.getMessage().contains("expecting >= 0"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testNegativeRowsAllowed() throws Exception {
		Object[] o = setup(dbType(true, true));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(-1);
		stmt.close();
		replay(cs, conn, stmt);
		assertEquals(1, SchemaUtils.createSchema(cs, "schema"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testExecuteThrows() throws Exception {
		Object[] o = setup(dbType(false, false));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andThrow(new SQLException("boom"));
		stmt.close();
		replay(cs, conn, stmt);
		SQLException e = assertThrows(SQLException.class, () -> SchemaUtils.createSchema(cs, "schema"));
		assertTrue(e.getMessage().startsWith("SQL statement failed"));
		verify(cs, conn, stmt);
	}

	@Test
	public void testCompileThrows() throws Exception {
		Object[] o = setup(dbType(false, false));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andThrow(new SQLException("boom"));
		replay(cs, conn);
		assertThrows(SQLException.class, () -> SchemaUtils.createSchema(cs, "schema"));
		verify(cs, conn);
	}

	@Test
	public void testCloseThrows() throws Exception {
		Object[] o = setup(dbType(false, false));
		ConnectionSource cs = (ConnectionSource) o[0];
		DatabaseConnection conn = (DatabaseConnection) o[1];
		CompiledStatement stmt = (CompiledStatement) o[2];
		expect(conn.compileStatement(anyObject(String.class), eq(StatementType.EXECUTE),
				anyObject(FieldType[].class), anyInt(), eq(false))).andReturn(stmt);
		expect(stmt.runExecute()).andReturn(0);
		stmt.close();
		expectLastCall().andThrow(new Exception("close"));
		replay(cs, conn, stmt);
		SQLException e = assertThrows(SQLException.class, () -> SchemaUtils.createSchema(cs, "schema"));
		assertTrue(e.getMessage().contains("could not close"));
		verify(cs, conn, stmt);
	}
}

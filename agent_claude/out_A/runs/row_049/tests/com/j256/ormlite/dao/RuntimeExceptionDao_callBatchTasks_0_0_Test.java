package com.j256.ormlite.dao;

import static org.easymock.EasyMock.*;
import static org.junit.jupiter.api.Assertions.*;

import java.sql.SQLException;
import java.util.concurrent.Callable;

import org.junit.jupiter.api.Test;

public class RuntimeExceptionDao_callBatchTasks_0_0_Test {

	@SuppressWarnings("unchecked")
	@Test
	public void testSuccess() throws Exception {
		Dao<Object, Object> dao = createMock(Dao.class);
		Callable<String> callable = () -> "result";
		expect(dao.callBatchTasks(callable)).andReturn("result");
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		assertEquals("result", rdao.callBatchTasks(callable));
		verify(dao);
	}

	@SuppressWarnings("unchecked")
	@Test
	public void testSqlException() throws Exception {
		Dao<Object, Object> dao = createMock(Dao.class);
		Callable<String> callable = () -> "x";
		SQLException ex = new SQLException("boom");
		expect(dao.callBatchTasks(callable)).andThrow(ex);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		RuntimeException re = assertThrows(RuntimeException.class, () -> rdao.callBatchTasks(callable));
		assertSame(ex, re.getCause());
		verify(dao);
	}

	@SuppressWarnings("unchecked")
	@Test
	public void testRuntimeException() throws Exception {
		Dao<Object, Object> dao = createMock(Dao.class);
		Callable<String> callable = () -> "x";
		IllegalStateException ex = new IllegalStateException("boom");
		expect(dao.callBatchTasks(callable)).andThrow(ex);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		RuntimeException re = assertThrows(RuntimeException.class, () -> rdao.callBatchTasks(callable));
		assertSame(ex, re.getCause());
		verify(dao);
	}

	@Test
	public void testRealCallableWithNullReturn() throws Exception {
		@SuppressWarnings("unchecked")
		Dao<Object, Object> dao = createMock(Dao.class);
		Callable<Void> callable = () -> null;
		expect(dao.callBatchTasks(callable)).andReturn(null);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		assertNull(rdao.callBatchTasks(callable));
		verify(dao);
	}
}

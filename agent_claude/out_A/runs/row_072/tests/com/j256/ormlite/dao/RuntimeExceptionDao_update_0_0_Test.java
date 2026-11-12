package com.j256.ormlite.dao;

import static org.easymock.EasyMock.createMock;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.sql.SQLException;

import org.junit.jupiter.api.Test;

public class RuntimeExceptionDao_update_0_0_Test {

	@Test
	@SuppressWarnings("unchecked")
	public void testUpdateSuccess() throws Exception {
		Dao<String, Integer> dao = createMock(Dao.class);
		expect(dao.update("foo")).andReturn(1);
		replay(dao);
		RuntimeExceptionDao<String, Integer> rdao = new RuntimeExceptionDao<String, Integer>(dao);
		assertEquals(1, rdao.update("foo"));
		verify(dao);
	}

	@Test
	@SuppressWarnings("unchecked")
	public void testUpdateNull() throws Exception {
		Dao<String, Integer> dao = createMock(Dao.class);
		expect(dao.update((String) null)).andReturn(0);
		replay(dao);
		RuntimeExceptionDao<String, Integer> rdao = new RuntimeExceptionDao<String, Integer>(dao);
		assertEquals(0, rdao.update((String) null));
		verify(dao);
	}

	@Test
	@SuppressWarnings("unchecked")
	public void testUpdateThrows() throws Exception {
		Dao<String, Integer> dao = createMock(Dao.class);
		SQLException sqle = new SQLException("boom");
		expect(dao.update("foo")).andThrow(sqle);
		replay(dao);
		RuntimeExceptionDao<String, Integer> rdao = new RuntimeExceptionDao<String, Integer>(dao);
		RuntimeException re = assertThrows(RuntimeException.class, () -> rdao.update("foo"));
		assertSame(sqle, re.getCause());
		verify(dao);
	}
}

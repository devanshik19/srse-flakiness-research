package com.j256.ormlite.dao;

import static org.easymock.EasyMock.createMock;
import static org.easymock.EasyMock.expectLastCall;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.sql.SQLException;

import org.junit.jupiter.api.Test;

public class RuntimeExceptionDao_assignEmptyForeignCollection_0_0_Test {

	@Test
	@SuppressWarnings("unchecked")
	public void testSuccess() throws Exception {
		Dao<Object, Object> dao = createMock(Dao.class);
		Object parent = new Object();
		dao.assignEmptyForeignCollection(parent, "field");
		expectLastCall();
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		rdao.assignEmptyForeignCollection(parent, "field");
		verify(dao);
	}

	@Test
	@SuppressWarnings("unchecked")
	public void testThrows() throws Exception {
		Dao<Object, Object> dao = createMock(Dao.class);
		Object parent = new Object();
		SQLException ex = new SQLException("boom");
		dao.assignEmptyForeignCollection(parent, "field");
		expectLastCall().andThrow(ex);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rdao = new RuntimeExceptionDao<Object, Object>(dao);
		RuntimeException re =
				assertThrows(RuntimeException.class, () -> rdao.assignEmptyForeignCollection(parent, "field"));
		assertSame(ex, re.getCause());
		verify(dao);
	}
}

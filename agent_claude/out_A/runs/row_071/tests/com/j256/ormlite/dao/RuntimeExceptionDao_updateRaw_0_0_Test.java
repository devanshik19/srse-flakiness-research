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

public class RuntimeExceptionDao_updateRaw_0_0_Test {

	@Test
	@SuppressWarnings("unchecked")
	public void testUpdateRawSuccess() throws Exception {
		Dao<Object, Object> dao = (Dao<Object, Object>) createMock(Dao.class);
		expect(dao.updateRaw("UPDATE foo SET x = 1")).andReturn(5);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rDao = new RuntimeExceptionDao<Object, Object>(dao);
		assertEquals(5, rDao.updateRaw("UPDATE foo SET x = 1"));
		verify(dao);
	}

	@Test
	@SuppressWarnings("unchecked")
	public void testUpdateRawThrows() throws Exception {
		Dao<Object, Object> dao = (Dao<Object, Object>) createMock(Dao.class);
		SQLException sqle = new SQLException("boom");
		expect(dao.updateRaw("bad")).andThrow(sqle);
		replay(dao);
		RuntimeExceptionDao<Object, Object> rDao = new RuntimeExceptionDao<Object, Object>(dao);
		RuntimeException ex = assertThrows(RuntimeException.class, () -> rDao.updateRaw("bad"));
		assertSame(sqle, ex.getCause());
		verify(dao);
	}
}

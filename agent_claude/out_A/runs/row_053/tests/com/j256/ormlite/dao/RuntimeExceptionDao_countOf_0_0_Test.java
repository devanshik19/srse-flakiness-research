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

import com.j256.ormlite.stmt.PreparedQuery;

public class RuntimeExceptionDao_countOf_0_0_Test {

	@SuppressWarnings("unchecked")
	@Test
	public void testCountOfSuccess() throws Exception {
		Dao<Object, Integer> dao = createMock(Dao.class);
		PreparedQuery<Object> pq = createMock(PreparedQuery.class);
		expect(dao.countOf(pq)).andReturn(42L);
		replay(dao, pq);
		RuntimeExceptionDao<Object, Integer> rDao = new RuntimeExceptionDao<Object, Integer>(dao);
		assertEquals(42L, rDao.countOf(pq));
		verify(dao);
	}

	@SuppressWarnings("unchecked")
	@Test
	public void testCountOfZero() throws Exception {
		Dao<Object, Integer> dao = createMock(Dao.class);
		expect(dao.countOf((PreparedQuery<Object>) null)).andReturn(0L);
		replay(dao);
		RuntimeExceptionDao<Object, Integer> rDao = new RuntimeExceptionDao<Object, Integer>(dao);
		assertEquals(0L, rDao.countOf((PreparedQuery<Object>) null));
		verify(dao);
	}

	@SuppressWarnings("unchecked")
	@Test
	public void testCountOfThrows() throws Exception {
		Dao<Object, Integer> dao = createMock(Dao.class);
		PreparedQuery<Object> pq = createMock(PreparedQuery.class);
		SQLException sqle = new SQLException("boom");
		expect(dao.countOf(pq)).andThrow(sqle);
		replay(dao, pq);
		RuntimeExceptionDao<Object, Integer> rDao = new RuntimeExceptionDao<Object, Integer>(dao);
		RuntimeException re = assertThrows(RuntimeException.class, () -> rDao.countOf(pq));
		assertSame(sqle, re.getCause());
		verify(dao);
	}
}

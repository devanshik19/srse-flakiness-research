package org.apache.camel.support.task;

import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.camel.support.task.budget.TimeBoundedBudget;
import org.apache.camel.support.task.budget.TimeBudget;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import static org.junit.jupiter.api.Assertions.*;

public class BackgroundTask_run_0_0_Test {

    static class TestBudget implements TimeBudget {
        final long maxDuration;
        final boolean next;

        TestBudget(long maxDuration, boolean next) {
            this.maxDuration = maxDuration;
            this.next = next;
        }

        public long maxDuration() {
            return maxDuration;
        }

        public long initialDelay() {
            return 0;
        }

        public long interval() {
            return 10;
        }

        public boolean canContinue() {
            return true;
        }

        public boolean next() {
            return next;
        }

        public Duration elapsed() {
            return Duration.ZERO;
        }
    }

    private BackgroundTask task(TimeBudget b, ScheduledExecutorService s) {
        return new BackgroundTask(b, s, "test");
    }

    @Test
    @Timeout(10)
    public void unlimitedSucceeds() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        AtomicInteger c = new AtomicInteger();
        assertTrue(task(new TestBudget(TimeBoundedBudget.UNLIMITED_DURATION, true), s)
                .run(() -> c.incrementAndGet() >= 3));
        assertTrue(s.isShutdown());
        assertTrue(c.get() >= 3);
    }

    @Test
    @Timeout(10)
    public void limitedSucceeds() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        assertTrue(task(new TestBudget(5000, true), s).run(() -> true));
        assertTrue(s.isShutdown());
    }

    @Test
    @Timeout(10)
    public void limitedTimesOut() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        assertFalse(task(new TestBudget(200, true), s).run(() -> false));
        assertTrue(s.isShutdown());
    }

    @Test
    @Timeout(10)
    public void noBudget() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        AtomicInteger c = new AtomicInteger();
        assertFalse(task(new TestBudget(200, false), s).run(() -> {
            c.incrementAndGet();
            return true;
        }));
        assertEquals(0, c.get());
    }

    @Test
    public void interrupted() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        Thread.currentThread().interrupt();
        try {
            assertFalse(task(new TestBudget(5000, true), s).run(() -> false));
            assertTrue(s.isShutdown());
        } finally {
            Thread.interrupted();
        }
    }

    @Test
    public void interruptedUnlimited() {
        ScheduledExecutorService s = Executors.newSingleThreadScheduledExecutor();
        Thread.currentThread().interrupt();
        try {
            assertFalse(task(new TestBudget(TimeBoundedBudget.UNLIMITED_DURATION, true), s).run(() -> false));
        } finally {
            Thread.interrupted();
        }
    }

    @Test
    public void nullService() {
        assertThrows(NullPointerException.class, () -> new BackgroundTask(new TestBudget(1, true), null, "x"));
    }
}

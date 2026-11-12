package com.epam.eco.schemacatalog.store.metadata;

import static org.junit.Assert.*;

import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.epam.eco.schemacatalog.domain.metadata.FieldMetadataKey;
import com.epam.eco.schemacatalog.domain.metadata.MetadataKey;
import com.epam.eco.schemacatalog.domain.metadata.MetadataValue;
import com.epam.eco.schemacatalog.domain.metadata.SchemaMetadataKey;

public class InheritingMetadataContainer_remove_0_0_Test {

    private static final String SUBJECT = "subj";
    private InheritingMetadataContainer container;

    private static MetadataValue value(String doc) {
        return MetadataValue.builder().doc(doc).build();
    }

    @Before
    public void setUp() {
        container = new InheritingMetadataContainer(SUBJECT);
    }

    @Test(expected = NullPointerException.class)
    public void testNullKey() {
        container.remove(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testWrongSubject() {
        container.remove(SchemaMetadataKey.with("other", 1));
    }

    @Test
    public void testMissingVersion() {
        assertNull(container.remove(SchemaMetadataKey.with(SUBJECT, 1)));
        assertTrue(container.isEmpty());
    }

    @Test
    public void testMissingKeyInExistingVersion() {
        container.put(SchemaMetadataKey.with(SUBJECT, 1), value("a"));
        assertNull(container.remove(FieldMetadataKey.with(SUBJECT, 1, "S", "f")));
        assertFalse(container.isEmpty());
    }

    @Test
    public void testRemoveOnlyKeyRemovesVersion() {
        MetadataKey key = SchemaMetadataKey.with(SUBJECT, 1);
        MetadataValue v = value("a");
        container.put(key, v);
        assertEquals(v, container.remove(key));
        assertTrue(container.isEmpty());
        assertNull(container.getCollection(1));
    }

    @Test
    public void testRemoveKeepsVersionWithOtherOwnKeys() {
        MetadataKey key = SchemaMetadataKey.with(SUBJECT, 1);
        MetadataKey field = FieldMetadataKey.with(SUBJECT, 1, "S", "f");
        container.put(key, value("a"));
        container.put(field, value("b"));
        assertEquals(value("a"), container.remove(key));
        Map<MetadataKey, MetadataValue> c = container.getCollection(1);
        assertNotNull(c);
        assertEquals(1, c.size());
        assertEquals(value("b"), c.get(field));
    }

    @Test
    public void testRemoveTakesBackInheritance() {
        MetadataKey key1 = SchemaMetadataKey.with(SUBJECT, 1);
        MetadataKey field3 = FieldMetadataKey.with(SUBJECT, 3, "S", "f");
        container.put(key1, value("a"));
        container.put(field3, value("b"));
        assertEquals(2, container.getCollection(3).size());
        assertEquals(value("a"), container.remove(key1));
        assertNull(container.getCollection(1));
        Map<MetadataKey, MetadataValue> c = container.getCollection(3);
        assertEquals(1, c.size());
        assertEquals(value("b"), c.get(field3));
    }

    @Test
    public void testRemoveInheritedKeyReturnsNull() {
        container.put(SchemaMetadataKey.with(SUBJECT, 1), value("a"));
        container.put(FieldMetadataKey.with(SUBJECT, 2, "S", "f"), value("b"));
        assertNull(container.remove(SchemaMetadataKey.with(SUBJECT, 2)));
        assertEquals(2, container.getCollection(2).size());
    }

    @Test
    public void testRemoveOverrideRestoresParentInheritance() {
        MetadataKey key1 = SchemaMetadataKey.with(SUBJECT, 1);
        MetadataKey key2 = SchemaMetadataKey.with(SUBJECT, 2);
        MetadataKey field3 = FieldMetadataKey.with(SUBJECT, 3, "S", "f");
        container.put(key1, value("a"));
        container.put(key2, value("b"));
        container.put(field3, value("c"));
        assertEquals(value("b"), container.getCollection(3).get(key2));

        assertEquals(value("b"), container.remove(key2));
        assertEquals(value("a"), container.getCollection(2).get(key1));
        Map<MetadataKey, MetadataValue> c3 = container.getCollection(3);
        assertEquals(value("a"), c3.get(key1));
        assertEquals(value("c"), c3.get(field3));
        assertEquals(2, c3.size());
    }

    @Test
    public void testRemoveTwice() {
        MetadataKey key = SchemaMetadataKey.with(SUBJECT, 5);
        container.put(key, value("a"));
        assertNotNull(container.remove(key));
        assertNull(container.remove(key));
    }
}

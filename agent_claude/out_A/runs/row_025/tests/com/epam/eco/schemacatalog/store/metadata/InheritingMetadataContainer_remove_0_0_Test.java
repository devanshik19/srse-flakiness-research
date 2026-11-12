package com.epam.eco.schemacatalog.store.metadata;

import java.util.Date;
import java.util.Map;

import org.junit.Assert;
import org.junit.Test;

import com.epam.eco.schemacatalog.domain.metadata.FieldMetadataKey;
import com.epam.eco.schemacatalog.domain.metadata.MetadataKey;
import com.epam.eco.schemacatalog.domain.metadata.MetadataValue;

public class InheritingMetadataContainer_remove_0_0_Test {

    private static MetadataValue value(String doc) {
        return MetadataValue.builder().doc(doc).attributes(null)
                .updatedAt(new Date()).updatedBy("me").build();
    }

    @Test(expected = NullPointerException.class)
    public void testNullKey() {
        new InheritingMetadataContainer("s").remove(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testWrongSubject() {
        new InheritingMetadataContainer("s").remove(new FieldMetadataKey("other", 1, "sfn", "f"));
    }

    @Test
    public void testRemoveFromEmpty() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        Assert.assertNull(c.remove(new FieldMetadataKey("s", 1, "sfn", "f")));
        Assert.assertTrue(c.isEmpty());
    }

    @Test
    public void testRemoveMissingKeyInExistingVersion() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataValue v = value("d");
        c.put(new FieldMetadataKey("s", 1, "sfn", "f1"), v);
        Assert.assertNull(c.remove(new FieldMetadataKey("s", 1, "sfn", "f2")));
        Assert.assertEquals(v, c.get(new FieldMetadataKey("s", 1, "sfn", "f1")));
    }

    @Test
    public void testRemoveInheritedKeyFromChildVersionReturnsNull() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        c.put(new FieldMetadataKey("s", 1, "sfn", "f1"), value("d1"));
        c.put(new FieldMetadataKey("s", 3, "sfn", "f2"), value("d3"));
        // key with version 3 for f1 doesn't exist (inherited key is version 1)
        Assert.assertNull(c.remove(new FieldMetadataKey("s", 3, "sfn", "f1")));
    }

    @Test
    public void testRemoveSingleKeyEmptiesContainer() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataKey k = new FieldMetadataKey("s", 1, "sfn", "f");
        MetadataValue v = value("d");
        c.put(k, v);
        Assert.assertEquals(v, c.remove(k));
        Assert.assertTrue(c.isEmpty());
        Assert.assertNull(c.get(k));
        Assert.assertNull(c.remove(k));
    }

    @Test
    public void testRemoveKeepsVersionWithOtherKeys() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataKey k1 = new FieldMetadataKey("s", 1, "sfn", "f1");
        MetadataKey k2 = new FieldMetadataKey("s", 1, "sfn", "f2");
        MetadataValue v1 = value("d1");
        MetadataValue v2 = value("d2");
        c.put(k1, v1);
        c.put(k2, v2);
        Assert.assertEquals(v1, c.remove(k1));
        Assert.assertFalse(c.isEmpty());
        Map<MetadataKey, MetadataValue> coll = c.getCollection(1);
        Assert.assertEquals(1, coll.size());
        Assert.assertEquals(v2, coll.get(k2));
    }

    @Test
    public void testRemoveTakesBackInheritance() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataKey k1 = new FieldMetadataKey("s", 1, "sfn", "f1");
        MetadataKey k3 = new FieldMetadataKey("s", 3, "sfn", "f2");
        MetadataKey k5 = new FieldMetadataKey("s", 5, "sfn", "f3");
        MetadataValue v1 = value("d1");
        c.put(k1, v1);
        c.put(k3, value("d3"));
        c.put(k5, value("d5"));
        Assert.assertTrue(c.getCollection(5).containsKey(k1));

        Assert.assertEquals(v1, c.remove(k1));
        Assert.assertNull(c.getCollection(1));
        Assert.assertFalse(c.getCollection(3).containsKey(k1));
        Assert.assertFalse(c.getCollection(5).containsKey(k1));
        Assert.assertEquals(1, c.getCollection(3).size());
        Assert.assertEquals(2, c.getCollection(5).size());
    }

    @Test
    public void testRemoveOverrideRestoresParentValue() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataKey k1 = new FieldMetadataKey("s", 1, "sfn", "f1");
        MetadataKey k3 = new FieldMetadataKey("s", 3, "sfn", "f1");
        MetadataKey k3b = new FieldMetadataKey("s", 3, "sfn", "f2");
        MetadataKey k5 = new FieldMetadataKey("s", 5, "sfn", "f3");
        MetadataValue v1 = value("d1");
        MetadataValue v3 = value("d3");
        c.put(k1, v1);
        c.put(k3b, value("d3b"));
        c.put(k5, value("d5"));
        c.put(k3, v3);

        Assert.assertEquals(v3, c.remove(k3));
        Assert.assertEquals(v1, c.getCollection(3).get(k1));
        Assert.assertEquals(v1, c.getCollection(5).get(k1));
    }

    @Test
    public void testRemoveOverrideVersionEmptied() {
        InheritingMetadataContainer c = new InheritingMetadataContainer("s");
        MetadataKey k1 = new FieldMetadataKey("s", 1, "sfn", "f1");
        MetadataKey k3 = new FieldMetadataKey("s", 3, "sfn", "f1");
        MetadataValue v1 = value("d1");
        MetadataValue v3 = value("d3");
        c.put(k1, v1);
        c.put(k3, v3);
        Assert.assertEquals(v3, c.remove(k3));
        Assert.assertEquals(v1, c.getCollection(3).get(k1));
        Assert.assertEquals(1, c.getCollection(3).size());
    }
}

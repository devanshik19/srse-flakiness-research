package org.apache.shardingsphere.elasticjob.infra.json;

import com.google.gson.Gson;
import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertTrue;

public final class GsonFactory_registerTypeAdapter_0_0_Test {
    
    static final class FooType {
        private String value = "x";
    }
    
    static final class BarType {
        private String name;
    }
    
    @Test
    public void assertRegisterTypeAdapterCreatesNewGson() {
        Gson before = GsonFactory.getGson();
        assertEquals("{\"value\":\"x\"}", before.toJson(new FooType()));
        GsonFactory.registerTypeAdapter(FooType.class, new TypeAdapter<FooType>() {
            
            @Override
            public void write(final JsonWriter out, final FooType value) throws IOException {
                out.value("foo");
            }
            
            @Override
            public FooType read(final JsonReader in) throws IOException {
                in.skipValue();
                return new FooType();
            }
        });
        Gson after = GsonFactory.getGson();
        assertNotSame(before, after);
        assertEquals("{\"value\":\"x\"}", before.toJson(new FooType()));
        assertEquals("\"foo\"", after.toJson(new FooType()));
        assertNotNull(after.fromJson("\"anything\"", FooType.class));
    }
    
    @Test
    public void assertRegisterTypeAdapterForRead() {
        GsonFactory.registerTypeAdapter(BarType.class, new TypeAdapter<BarType>() {
            
            @Override
            public void write(final JsonWriter out, final BarType value) throws IOException {
                out.value(value.name);
            }
            
            @Override
            public BarType read(final JsonReader in) throws IOException {
                BarType result = new BarType();
                result.name = in.nextString() + "!";
                return result;
            }
        });
        BarType bar = GsonFactory.getGson().fromJson("\"abc\"", BarType.class);
        assertEquals("abc!", bar.name);
        assertEquals("\"abc!\"", GsonFactory.getGson().toJson(bar));
    }
    
    @Test
    public void assertPrivateConstructor() throws Exception {
        Constructor<GsonFactory> constructor = GsonFactory.class.getDeclaredConstructor();
        assertTrue(Modifier.isPrivate(constructor.getModifiers()));
        constructor.setAccessible(true);
        assertNotNull(constructor.newInstance());
    }
}

package org.apache.fury.codegen;

import static org.testng.Assert.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.apache.fury.codegen.Expression.Literal;
import org.apache.fury.reflect.TypeRef;
import org.testng.annotations.Test;

public class ExpressionVisitor_traverseExpression_0_0_Test {

  @Test(expectedExceptions = NullPointerException.class)
  public void testNullExpr() {
    new ExpressionVisitor().traverseExpression(null, s -> true);
  }

  @Test
  public void testStopTraverse() {
    Literal a = Literal.ofInt(1);
    Literal b = Literal.ofInt(2);
    Expression.Arithmetic add = new Expression.Arithmetic(true, "+", a, b);
    List<ExpressionVisitor.ExprSite> sites = new ArrayList<>();
    new ExpressionVisitor()
        .traverseExpression(
            add,
            s -> {
              sites.add(s);
              return false;
            });
    assertEquals(1, sites.size());
    assertSame(add, sites.get(0).current);
    assertNull(sites.get(0).parent);
  }

  @Test
  public void testFullTraverse() {
    Literal a = Literal.ofInt(1);
    Literal b = Literal.ofInt(2);
    Expression.Arithmetic add = new Expression.Arithmetic(true, "+", a, b);
    List<Expression> exprs = new ArrayList<>();
    new ExpressionVisitor().traverseExpression(add, s -> exprs.add(s.current));
    assertEquals(Arrays.asList(add, a, b), exprs);
  }

  @Test
  public void testListExpression() {
    Literal a = Literal.ofInt(1);
    Expression.Reference ref = new Expression.Reference("x", TypeRef.of(Object.class));
    Expression.ListExpression list = new Expression.ListExpression(a, ref);
    List<Expression> exprs = new ArrayList<>();
    new ExpressionVisitor().traverseExpression(list, s -> exprs.add(s.current));
    assertEquals(Arrays.asList(list, a, ref), exprs);
  }

  @Test
  public void testLeaf() {
    Literal a = Literal.ofInt(1);
    List<Expression> exprs = new ArrayList<>();
    new ExpressionVisitor().traverseExpression(a, s -> exprs.add(s.current));
    assertEquals(Arrays.asList(a), exprs);
  }
}

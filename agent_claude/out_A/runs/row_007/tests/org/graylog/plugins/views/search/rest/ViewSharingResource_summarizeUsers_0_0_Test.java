package org.graylog.plugins.views.search.rest;

import com.google.common.collect.ImmutableList;
import org.graylog.plugins.views.search.views.ViewService;
import org.graylog.plugins.views.search.views.sharing.UserShortSummary;
import org.graylog.plugins.views.search.views.sharing.ViewSharingService;
import org.graylog2.plugin.database.users.User;
import org.graylog2.shared.users.UserService;
import org.junit.Before;
import org.junit.Test;

import java.util.Collections;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class ViewSharingResource_summarizeUsers_0_0_Test {
    private ViewSharingService viewSharingService;
    private ViewService viewService;
    private UserService userService;
    private User currentUser;
    private ViewSharingResource resource;

    @Before
    public void setUp() {
        viewSharingService = mock(ViewSharingService.class);
        viewService = mock(ViewService.class);
        userService = mock(UserService.class);
        currentUser = mock(User.class);
        resource = new ViewSharingResource(viewSharingService, viewService, userService) {
            @Override
            protected User getCurrentUser() {
                return currentUser;
            }
        };
    }

    private User user(String name, String fullName) {
        final User u = mock(User.class);
        when(u.getName()).thenReturn(name);
        when(u.getFullName()).thenReturn(fullName);
        return u;
    }

    @Test
    public void excludesCurrentUser() {
        when(currentUser.getName()).thenReturn("peter");
        final User a = user("franz", "Franz");
        final User b = user("friedrich", "Friedrich");
        final User c = user("peter", "Peter");
        when(userService.loadAll()).thenReturn(ImmutableList.of(a, b, c));

        final Set<UserShortSummary> result = resource.summarizeUsers("id");

        assertThat(result).containsExactlyInAnyOrder(
                UserShortSummary.create("franz", "Franz"),
                UserShortSummary.create("friedrich", "Friedrich"));
    }

    @Test
    public void currentUserNullReturnsAll() {
        currentUser = null;
        final User a = user("franz", "Franz");
        final User b = user("peter", "Peter");
        when(userService.loadAll()).thenReturn(ImmutableList.of(a, b));

        final Set<UserShortSummary> result = resource.summarizeUsers("id");

        assertThat(result).containsExactlyInAnyOrder(
                UserShortSummary.create("franz", "Franz"),
                UserShortSummary.create("peter", "Peter"));
    }

    @Test
    public void emptyUserList() {
        when(currentUser.getName()).thenReturn("peter");
        when(userService.loadAll()).thenReturn(Collections.emptyList());

        assertThat(resource.summarizeUsers("id")).isEmpty();
    }

    @Test
    public void onlyCurrentUser() {
        when(currentUser.getName()).thenReturn("peter");
        final User p = user("peter", "Peter");
        when(userService.loadAll()).thenReturn(ImmutableList.of(p));

        assertThat(resource.summarizeUsers("id")).isEmpty();
    }
}

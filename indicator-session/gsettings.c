/* Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to> */

/* A test program for the code in 0003_Workaround_disappearing_icon.patch */
/* Compile with:
 *   gcc gsettings.c $(pkg-config --cflags --libs glib-2.0 gio-2.0) */

#include <glib.h>
#include <gio/gio.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
  g_type_init();

  gboolean okay = FALSE;

  /* The system-devices-panel and system-shutdown-panel icons are only available
   * in Ubuntu's monochrome icon themes. We'll fall back to the system-shutdown
   * icon for other icon themes */
  GSettings * get_stuff = g_settings_new("org.gnome.desktop.interface");
  gchar * icon_theme = g_settings_get_string(get_stuff, "icon-theme");
  printf("Icon Theme: %s\n", icon_theme);
  if (g_strcmp0(icon_theme, "ubuntu-mono-dark") == 0 ||
      g_strcmp0(icon_theme, "ubuntu-mono-light") == 0) {
    okay = TRUE;
    printf("Icon theme is Ubuntu's\n");
  }

  /* If the theme inherits the Ubuntu monochrome icon themes, that's okay too */
  GKeyFile * icon_theme_index = g_key_file_new();
  gchar * icon_theme_path = g_strconcat("/usr/share/icons/",
                                        icon_theme,
                                        "/index.theme",
                                        NULL);
  printf("Icon path: %s\n", icon_theme_path);
  if (g_key_file_load_from_file(icon_theme_index,
                                icon_theme_path,
                                G_KEY_FILE_NONE, NULL)) {
    gchar * icon_theme_inherits = g_key_file_get_string(icon_theme_index,
                                                        "Icon Theme",
                                                        "Inherits",
                                                        NULL);
    printf("Inherits: %s\n", icon_theme_inherits);
    if (icon_theme_inherits != NULL) {
      if (g_strstr_len(icon_theme_inherits, -1, "ubuntu-mono-dark") != NULL ||
          g_strstr_len(icon_theme_inherits, -1, "ubuntu-mono-light") != NULL) {
        okay = TRUE;
      }
    }
    g_free(icon_theme_inherits);
  }
  g_free(icon_theme_path);
  g_key_file_free(icon_theme_index);
  g_free(icon_theme);
  
  if (okay == TRUE) {
    printf("Using Ubuntu mono\n");
  }
  else {
    printf("Using another theme\n");
  }
}

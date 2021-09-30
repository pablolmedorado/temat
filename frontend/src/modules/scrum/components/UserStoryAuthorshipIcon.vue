<template>
  <v-menu :close-on-content-click="false" :nudge-width="200" open-on-hover offset-y bottom>
    <template #activator="{ on, attrs }">
      <v-icon v-bind="attrs" class="authorship-icon" v-on="on">mdi-account-edit</v-icon>
    </template>
    <v-card>
      <v-card-title class="text-h6"> Autoría </v-card-title>
      <v-card-text>
        <v-simple-table>
          <template #default>
            <thead>
              <tr>
                <th class="text-left">Acción</th>
                <th class="text-left">Usuario</th>
                <th class="text-left">Fecha</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Creación</td>
                <td><UserPill :user="userStory.creation_user" /></td>
                <td>{{ userStory.creation_datetime | datetime }}</td>
              </tr>
              <tr>
                <td>Modificación</td>
                <td>
                  <UserPill v-if="userStory.modification_user" :user="userStory.modification_user" />
                </td>
                <td>
                  <span v-if="userStory.modification_user">
                    {{ userStory.modification_datetime | datetime }}
                  </span>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "UserStoryAuthorshipIcon",
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  inheritAttrs: false,
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.authorship-icon {
  cursor: help !important;
}
</style>

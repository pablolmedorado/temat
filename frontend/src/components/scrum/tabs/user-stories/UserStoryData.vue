<template>
  <div>
    <v-row v-if="item.id" class="mb-2">
      <v-col>
        <v-card>
          <v-card-title class="text-h6">
            Estado
            <v-spacer />
            <v-tooltip left>
              <template #activator="{ on, attrs }">
                <v-icon v-if="item.validated === false" class="mr-2" color="error" v-bind="attrs" v-on="on">
                  mdi-alert-circle-check-outline
                </v-icon>
              </template>
              <span> Fecha de rechazo: {{ item.validated_changed | datetime }} </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-icon :color="riskLevelsMap[item.risk_level].colour" v-bind="attrs" v-on="on">
                  {{ riskLevelsMap[item.risk_level].icon }}
                </v-icon>
              </template>
              <span> Nivel de riesgo ({{ riskLevelsMap[item.risk_level].label }}) </span>
            </v-tooltip>
          </v-card-title>
          <v-card-text>
            <UserStoryStatus :user-story="item" />
            <UserStoryProgressBar :user-story="item" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <UserStoryForm ref="userStoryForm" :source-item="item" @changed:item="$emit('changed:item', $event)" />

    <v-speed-dial
      v-if="canEdit"
      v-model="showSpeedDial"
      fixed
      bottom
      right
      direction="top"
      open-on-hover
      transition="slide-y-reverse-transition"
    >
      <template #activator>
        <v-btn fab dark color="secondary" @click="saveUserStory">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </template>
      <v-btn
        v-if="item.id && item.status === 3 && canValidate"
        fab
        dark
        small
        color="green"
        @click="validateUserStory(item)"
      >
        <v-icon>mdi-check-bold</v-icon>
      </v-btn>
      <v-btn fab dark small color="orange" @click="resetForm">
        <v-icon>mdi-restore</v-icon>
      </v-btn>
      <v-btn v-if="item.id && canCopy" fab dark small color="secondary" @click="copyUserStory">
        <v-icon>mdi-content-copy</v-icon>
      </v-btn>
      <v-btn v-if="item.id && canDelete" fab dark small color="red" @click.stop="openDeleteDialog(item)">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>

    <DeletionConfirmationDialog ref="deleteDialog" child-elements-warning @confirm="deleteUserStory" />
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import UserStory from "@/models/scrum/user-story";

import UserStoryService from "@/services/scrum/user-story-service";

import UserStoryForm from "@/components/scrum/forms/UserStoryForm";
import UserStoryProgressBar from "@/components/scrum/UserStoryProgressBar";
import UserStoryStatus from "@/components/scrum/UserStoryStatus";

import { isoDateTimeToLocaleString } from "@/utils/dates";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "UserStoryData",
  components: { UserStoryForm, UserStoryProgressBar, UserStoryStatus },
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showSpeedDial: false,
      showdeleteUserStoryDialog: false,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters("scrum", ["riskLevelsMap"]),
    canEdit() {
      const action = this.item.id ? "change" : "add";
      return (
        [this.item.development_user, this.item.validation_user, this.item.support_user].includes(this.loggedUser.id) ||
        userHasPermission(`scrum.${action}_userstory`)
      );
    },
    canValidate() {
      return this.loggedUser.id === this.item.validation_user || userHasPermission(UserStory.CHANGE_PERMISSION);
    },
    canCopy() {
      return userHasPermission(UserStory.ADD_PERMISSION);
    },
    canDelete() {
      return userHasPermission(UserStory.DELETE_PERMISSION);
    },
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    async saveUserStory() {
      const newUserStory = await this.$refs.userStoryForm.submit();
      if (newUserStory) {
        if (this.item.id) {
          this.$emit("update:item", newUserStory);
        } else {
          this.$emit("changed:item", false);
          this.$router.push({ name: "user-story", params: { id: newUserStory.id } });
        }
      }
    },
    async validateUserStory(item) {
      const response = await UserStoryService.validate(item.id, { expand: "sprint" });
      this.$emit("update:item", response.data);
    },
    async copyUserStory() {
      const response = await UserStoryService.copy(this.item.id);
      this.showSnackbar({
        color: "success",
        message: "Copia creada correctamente",
      });
      this.$router.push({ name: "user-story", params: { id: response.data.id } });
    },
    async deleteUserStory(item) {
      await UserStoryService.delete(item.id);
      this.$router.push({ name: "user-stories" });
    },
    resetForm() {
      this.$refs.userStoryForm.reset();
    },
    openDeleteDialog(item) {
      this.$refs.deleteDialog.open(item);
    },
  },
};
</script>

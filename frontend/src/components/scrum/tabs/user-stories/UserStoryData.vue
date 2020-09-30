<template>
  <div>
    <v-row v-if="item.id">
      <v-col>
        <v-card>
          <v-card-title class="text-h6">
            Estado
            <v-spacer></v-spacer>
            <v-tooltip left>
              <template v-slot:activator="{ on, attrs }">
                <v-icon v-if="item.validated === false" class="mr-2" color="error" v-bind="attrs" v-on="on">
                  mdi-alert-circle-check-outline
                </v-icon>
              </template>
              <span> Fecha de rechazo: {{ item.validated_changed | datetime }} </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
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

    <UserStoryForm ref="userStoryForm" :source-item="item" />

    <v-speed-dial
      v-if="!readOnly"
      v-model="showSpeedDial"
      fixed
      bottom
      right
      direction="top"
      :open-on-hover="true"
      transition="slide-y-reverse-transition"
    >
      <template v-slot:activator>
        <v-btn fab dark color="secondary" @click="saveUserStory">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </template>
      <v-btn
        v-if="item.id && item.status === 3 && (loggedUser.is_staff || item.validation_user === loggedUser.id)"
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
      <v-btn v-if="item.id && loggedUser.is_staff" fab dark small color="secondary" @click="copyUserStory">
        <v-icon>mdi-content-copy</v-icon>
      </v-btn>
      <v-btn v-if="item.id && loggedUser.is_staff" fab dark small color="red" @click.stop="openDeleteDialog(item)">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>

    <DeletionConfirmationDialog ref="deleteDialog" child-elements-warning @confirm="deleteUserStory" />
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

import UserStoryService from "@/services/scrum/user-story-service";

import UserStoryForm from "@/components/scrum/forms/UserStoryForm";
import UserStoryProgressBar from "@/components/scrum/UserStoryProgressBar";
import UserStoryStatus from "@/components/scrum/UserStoryStatus";

import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "UserStoryData",
  components: { UserStoryForm, UserStoryProgressBar, UserStoryStatus },
  filters: {
    datetime: isoDateTimeToLocaleString
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showSpeedDial: false,
      showdeleteUserStoryDialog: false
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters("scrum", ["riskLevelsMap"]),
    readOnly() {
      return (
        !this.loggedUser.is_staff &&
        ![this.item.development_user, this.item.validation_user, this.item.support_user].includes(this.loggedUser.id)
      );
    }
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    async saveUserStory() {
      const newUserStory = await this.$refs.userStoryForm.submit();
      if (newUserStory) {
        if (this.item.id) {
          this.$emit("update:item", newUserStory);
        } else {
          this.$router.push({ name: "user-story", params: { id: newUserStory.id } });
        }
      }
    },
    async validateUserStory(item) {
      const response = await UserStoryService.validate(item.id);
      this.$emit("update:item", response.data);
    },
    async copyUserStory() {
      const response = await UserStoryService.copy(this.item.id);
      this.showSnackbar({
        color: "success",
        message: "Copia creada correctamente"
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
    }
  }
};
</script>

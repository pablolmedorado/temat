<template>
  <div>
    <v-row v-if="item.id" class="mb-2">
      <v-col>
        <v-card>
          <v-card-title class="text-h6">
            Estado
            <v-spacer />
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-icon v-if="item.validated === false" class="mr-2" color="error" v-bind="attrs" v-on="on">
                  mdi-alert-circle-check-outline
                </v-icon>
              </template>
              <span> Fecha de rechazo: {{ item.validated_changed | datetime }} </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-icon :color="riskLevelsMap[item.risk_level].colour" v-bind="attrs" class="mr-2" v-on="on">
                  {{ riskLevelsMap[item.risk_level].icon }}
                </v-icon>
              </template>
              <span> Nivel de riesgo ({{ riskLevelsMap[item.risk_level].label }}) </span>
            </v-tooltip>
            <UserStoryAuthorshipIcon :user-story="item" />
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
import { computed, ref, toRefs } from "@vue/composition-api";

import UserStory from "@/modules/scrum/models/user-story";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";
import { useMainStore } from "@/stores/main";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import UserStoryForm from "@/modules/scrum/components/forms/UserStoryForm";
import UserStoryAuthorshipIcon from "@/modules/scrum/components/UserStoryAuthorshipIcon";
import UserStoryProgressBar from "@/modules/scrum/components/UserStoryProgressBar";
import UserStoryStatus from "@/modules/scrum/components/UserStoryStatus";

import { isoDateTimeToLocaleString } from "@/utils/dates";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "UserStoryData",
  components: { UserStoryAuthorshipIcon, UserStoryForm, UserStoryProgressBar, UserStoryStatus },
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit, refs, root }) {
    // Store
    const mainStore = useMainStore();
    const userStoryStore = useUserStoryStore();

    // State
    const showSpeedDial = ref(false);
    const showdeleteUserStoryDialog = ref(false);
    const canCopy = userHasPermission(UserStory.ADD_PERMISSION);
    const canDelete = userHasPermission(UserStory.DELETE_PERMISSION);

    // Computed
    const { riskLevelsMap } = toRefs(userStoryStore);
    const canEdit = computed(() => {
      const action = props.item.id ? "change" : "add";
      return (
        [props.item.development_user, props.item.validation_user, props.item.support_user].includes(
          mainStore.currentUser.id
        ) || userHasPermission(`scrum.${action}_userstory`)
      );
    });
    const canValidate = computed(() => {
      return mainStore.currentUser.id === props.item.validation_user || userHasPermission(UserStory.CHANGE_PERMISSION);
    });

    // Methods
    async function saveUserStory() {
      const newUserStory = await this.$refs.userStoryForm.submit();
      if (newUserStory) {
        if (props.item.id) {
          emit("update:item", newUserStory);
        } else {
          emit("changed:item", false);
          root.$router.push({ name: "user-story", params: { id: newUserStory.id } });
        }
      }
    }
    async function validateUserStory(item) {
      const response = await UserStoryService.validate(item.id, { expand: "sprint" });
      emit("update:item", response.data);
    }
    async function copyUserStory() {
      const response = await UserStoryService.copy(props.item.id);
      mainStore.showSnackbar({
        color: "success",
        message: "Copia creada correctamente",
      });
      root.$router.push({ name: "user-story", params: { id: response.data.id } });
    }
    async function deleteUserStory(item) {
      await UserStoryService.delete(item.id);
      root.$router.push({ name: "user-stories" });
    }
    function resetForm() {
      refs.userStoryForm.reset();
    }
    function openDeleteDialog(item) {
      refs.deleteDialog.open(item);
    }

    return {
      // State
      showSpeedDial,
      showdeleteUserStoryDialog,
      canCopy,
      canDelete,
      // Computed
      riskLevelsMap,
      canEdit,
      canValidate,
      // Methods
      saveUserStory,
      validateUserStory,
      copyUserStory,
      deleteUserStory,
      resetForm,
      openDeleteDialog,
    };
  },
};
</script>

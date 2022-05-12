<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="text-h6"> Información básica y clasificación </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" lg="8">
                <v-text-field
                  v-model="item.name"
                  label="Título*"
                  prepend-icon="mdi-format-title"
                  counter="500"
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.name)"
                />
              </v-col>
              <v-col cols="12" md="6" lg="4">
                <v-select
                  v-model.number="item.type"
                  :items="userStoryTypesOptions"
                  item-text="name"
                  item-value="id"
                  label="Tipo*"
                  prepend-icon="mdi-shape"
                  :loading="!userStoryTypesOptions.length"
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.type)"
                />
              </v-col>
              <v-col cols="12" md="6" lg="4">
                <AsyncAutocomplete
                  v-model="item.epic"
                  :service="epicService"
                  search-field="name"
                  search-lookup="icontains"
                  :readonly="!canEdit"
                  :clearable="canEdit"
                  label="Épica"
                  prepend-icon="mdi-sword-cross"
                >
                  <template v-if="item.epic" #append>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :to="{ name: 'epic-user-stories', params: { epicId: item.epic } }"
                          icon
                          small
                          v-on="onTooltip"
                        >
                          <v-icon> mdi-open-in-app </v-icon>
                        </v-btn>
                      </template>
                      <span> Ir a la épica </span>
                    </v-tooltip>
                  </template>
                </AsyncAutocomplete>
              </v-col>
              <v-col cols="12" lg="8">
                <TagAutocomplete
                  v-model="item.tags"
                  label="Tags"
                  prepend-icon="mdi-label"
                  :readonly="!canEdit"
                  multiple
                  chips
                  small-chips
                  deletable-chips
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="text-h6"> Descripción </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-textarea
                  v-model="item.functional_description"
                  label="Descripción funcional"
                  prepend-icon="mdi-text"
                  rows="10"
                  counter="2000"
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.functional_description)"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-textarea
                  v-model="item.technical_description"
                  label="Descripción técnica"
                  rows="10"
                  counter="2000"
                  prepend-icon="mdi-text"
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.technical_description)"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="item.external_resource"
                  label="Recurso externo"
                  prepend-icon="mdi-folder-network"
                  counter="2000"
                  hint="URL de fichero o directorio"
                  persistent-hint
                  :readonly="!canEdit && currentUser.id !== item.development_user"
                  :error-messages="getErrorMsgs(v$.item.external_resource)"
                >
                  <template v-if="canEdit || currentUser.id === item.development_user" #append>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-icon
                          v-bind="attrTooltip"
                          v-on="onTooltip"
                          @click="item.external_resource = encodeURI(item.external_resource)"
                        >
                          mdi-exit-run
                        </v-icon>
                      </template>
                      <span> Escapar url </span>
                    </v-tooltip>
                  </template>
                  <template
                    v-if="item.external_resource && (isWebUri(item.external_resource) || isClipboardSupported)"
                    #append-outer
                  >
                    <v-tooltip v-if="isWebUri(item.external_resource)" bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :href="item.external_resource"
                          target="_blank"
                          icon
                          v-on="onTooltip"
                        >
                          <v-icon> mdi-open-in-new </v-icon>
                        </v-btn>
                      </template>
                      <span> Abrir </span>
                    </v-tooltip>
                    <v-tooltip v-else bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn v-bind="attrTooltip" icon v-on="onTooltip" @click="copyExternalResourceToClipboard">
                          <v-icon> mdi-content-copy </v-icon>
                        </v-btn>
                      </template>
                      <span> Copiar al portapapeles </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="text-h6"> Planificación </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" lg="4">
                <AsyncAutocomplete
                  v-model="item.sprint"
                  :service="sprintService"
                  search-field="name"
                  search-lookup="icontains"
                  :readonly="!canEdit"
                  :clearable="canEdit"
                  :hint="item.sprint ? `Del ${item.sprint.start_date} al ${item.sprint.end_date}` : ''"
                  :persistent-hint="Boolean(item.sprint)"
                  label="Sprint"
                  prepend-icon="mdi-run-fast"
                  return-object
                  @click:clear="onSprintClear"
                >
                  <template v-if="item.sprint" #append>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :to="{
                            name: 'sprint-user-stories',
                            params: { sprintId: item.sprint.id },
                          }"
                          icon
                          small
                          v-on="onTooltip"
                        >
                          <v-icon> mdi-open-in-app </v-icon>
                        </v-btn>
                      </template>
                      <span> Ir al sprint </span>
                    </v-tooltip>
                  </template>
                </AsyncAutocomplete>
              </v-col>
              <v-col cols="12" sm="6" lg="4">
                <DatePickerInput
                  v-model="item.start_date"
                  label="Fecha de inicio planificada"
                  prepend-icon="mdi-calendar-start"
                  :readonly="!canEdit"
                  :clearable="canEdit"
                  :error-messages="getErrorMsgs(v$.item.start_date)"
                >
                  <template v-if="canEdit" #append>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :disabled="!canEdit"
                          icon
                          small
                          v-on="onTooltip"
                          @click="setStartDateFromSprint"
                        >
                          <v-icon> mdi-run-fast </v-icon>
                        </v-btn>
                      </template>
                      <span> Usar fecha del sprint </span>
                    </v-tooltip>
                  </template>
                </DatePickerInput>
              </v-col>
              <v-col cols="12" sm="6" lg="4">
                <DatePickerInput
                  v-model="item.end_date"
                  label="Fecha límite"
                  prepend-icon="mdi-calendar-end"
                  :readonly="!canEdit"
                  :clearable="canEdit"
                  :error-messages="getErrorMsgs(v$.item.end_date)"
                >
                  <template v-if="canEdit" #append>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :disabled="!canEdit"
                          icon
                          small
                          v-on="onTooltip"
                          @click="setEndDateFromSprint"
                        >
                          <v-icon> mdi-run-fast </v-icon>
                        </v-btn>
                      </template>
                      <span> Usar fecha del sprint </span>
                    </v-tooltip>
                  </template>
                </DatePickerInput>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" lg="4">
                <v-text-field
                  v-model.number="item.planned_effort"
                  label="Esfuerzo planificado*"
                  type="number"
                  min="1"
                  prepend-icon="mdi-dumbbell"
                  suffix="UT"
                  hint="1UT = 1/2h"
                  persistent-hint
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.planned_effort)"
                />
              </v-col>
              <v-col cols="12" sm="6" lg="4">
                <v-text-field
                  v-model.number="item.priority"
                  label="Prioridad*"
                  type="number"
                  min="1"
                  max="10"
                  prepend-icon="mdi-priority-high"
                  hint="Menor número, mayor importancia"
                  persistent-hint
                  :readonly="!canEdit"
                  :error-messages="getErrorMsgs(v$.item.priority)"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="text-h6"> Asignación </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title>Desarrollo</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col>
                        <UserAutocomplete
                          v-model.number="item.development_user"
                          label="Desarrollador"
                          prepend-icon="mdi-account"
                          :readonly="!canEdit"
                          :clearable="canEdit"
                          show-random-btn
                          :error-messages="getErrorMsgs(v$.item.development_user)"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-textarea
                          v-model="item.development_comments"
                          label="Comentarios del desarrollador"
                          counter="2000"
                          prepend-icon="mdi-comment-quote"
                          :readonly="!canEdit && currentUser.id !== item.development_user"
                          :error-messages="getErrorMsgs(v$.item.development_comments)"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-text-field
                          v-model.trim="item.cvs_branch_name"
                          label="Rama SCV"
                          counter="255"
                          prepend-icon="mdi-source-branch"
                          :readonly="!canEdit && currentUser.id !== item.development_user"
                          :error-messages="getErrorMsgs(v$.item.cvs_branch_name)"
                        >
                          <template #append>
                            <v-btn v-show="branchUrl" icon small :href="branchUrl" target="_blank">
                              <v-icon>{{ `mdi-${cvsVendor}` }}</v-icon>
                            </v-btn>
                          </template>
                        </v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" lg="6">
                        <v-text-field
                          v-model="item.cvs_issue_id"
                          label="Issue SCV"
                          prepend-icon="mdi-record-circle-outline"
                          prefix="#"
                          min="1"
                          :readonly="!canEdit && currentUser.id !== item.development_user"
                          :error-messages="getErrorMsgs(v$.item.cvs_issue_id)"
                        >
                          <template #append>
                            <v-btn v-show="issueUrl" icon small :href="issueUrl" target="_blank">
                              <v-icon>{{ `mdi-${cvsVendor}` }}</v-icon>
                            </v-btn>
                          </template>
                        </v-text-field>
                      </v-col>
                      <v-col cols="12" lg="6">
                        <v-text-field
                          v-model="item.cvs_pull_request_id"
                          label="Pull Request SCV"
                          prepend-icon="mdi-source-pull"
                          prefix="#"
                          min="1"
                          :readonly="!canEdit && currentUser.id !== item.development_user"
                          :error-messages="getErrorMsgs(v$.item.cvs_pull_request_id)"
                        >
                          <template #append>
                            <v-btn v-show="pullRequestUrl" icon small :href="pullRequestUrl" target="_blank">
                              <v-icon>{{ `mdi-${cvsVendor}` }}</v-icon>
                            </v-btn>
                          </template>
                        </v-text-field>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title>Validación</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col>
                        <UserAutocomplete
                          v-model.number="item.validation_user"
                          label="Validador"
                          prepend-icon="mdi-account-check"
                          :readonly="!canEdit"
                          :clearable="canEdit"
                          show-random-btn
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-textarea
                          v-model="item.validation_comments"
                          label="Comentarios del validador"
                          counter="2000"
                          prepend-icon="mdi-comment-quote"
                          :readonly="!canEdit && currentUser.id !== item.validation_user"
                          :error-messages="getErrorMsgs(v$.item.validation_comments)"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-select
                          v-model="item.validated"
                          :items="validatedOptions"
                          :disabled="item.status < 3"
                          :readonly="
                            !canEdit && ![item.development_user, item.validation_user].includes(currentUser.id)
                          "
                          :hint="validatedHintText"
                          persistent-hint
                          label="Estado"
                          prepend-icon="mdi-check-bold"
                        />
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title>Soporte</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col>
                        <UserAutocomplete
                          v-model.number="item.support_user"
                          label="Soporte"
                          prepend-icon="mdi-account-question"
                          :readonly="!canEdit"
                          :clearable="canEdit"
                          show-random-btn
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-textarea
                          v-model="item.support_comments"
                          label="Comentarios de soporte"
                          counter="2000"
                          prepend-icon="mdi-comment-quote"
                          :readonly="!canEdit && currentUser.id !== item.support_user"
                          :error-messages="getErrorMsgs(v$.item.support_comments)"
                        />
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-title class="text-h6"> Gestión de riesgo </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model.number="item.risk_level"
                  :items="riskLevelOptions"
                  item-text="label"
                  item-value="value"
                  label="Nivel de riesgo*"
                  prepend-icon="mdi-alert-decagram"
                  :readonly="!canEdit && !hasARole"
                  :error-messages="getErrorMsgs(v$.item.risk_level)"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="item.risk_comments"
                  label="Comentarios de riesgo"
                  counter="2000"
                  prepend-icon="mdi-comment-quote"
                  :readonly="!canEdit && !hasARole"
                  :error-messages="getErrorMsgs(v$.item.risk_comments)"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-title class="text-h6"> Información de despliegue </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model.number="item.use_migrations"
                  :items="useMigrationsOptions"
                  label="Usa migraciones*"
                  prepend-icon="mdi-database-arrow-right"
                  :readonly="!canEdit && currentUser.id !== item.development_user"
                  :error-messages="getErrorMsgs(v$.item.use_migrations)"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="item.deployment_notes"
                  label="Notas de despliegue"
                  counter="2000"
                  prepend-icon="mdi-note-text"
                  :readonly="!canEdit && currentUser.id !== item.development_user"
                  :error-messages="getErrorMsgs(v$.item.deployment_notes)"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { computed, toRefs } from "@vue/composition-api";
import { DateTime } from "luxon";
import { between, helpers, maxLength, minValue, numeric, required, requiredIf } from "@vuelidate/validators";
import { defaultTo } from "lodash-es";
import { isWebUri } from "valid-url";
import { useClipboard } from "@vueuse/core";

import EpicService from "@/modules/scrum/services/epic-service";
import SprintService from "@/modules/scrum/services/sprint-service";
import UserStoryService from "@/modules/scrum/services/user-story-service";

import { useMainStore } from "@/stores/main";
import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import { useForm, formProps } from "@/composables/form";
import { useUserStoryTypes } from "@/modules/scrum/composables/user-story-types";
import { isoDateTimeToLocaleString, isoDateToLocaleString } from "@/utils/dates";
import { userHasPermission } from "@/utils/permissions";
import { urlValidator } from "@/utils/validation";

export default {
  name: "UserStoryForm",
  filters: {
    date: isoDateToLocaleString,
  },
  props: formProps,
  validations() {
    return {
      item: {
        name: { required, maxLength: maxLength(500) },
        type: { required },
        functional_description: { maxLength: maxLength(2000) },
        technical_description: { maxLength: maxLength(2000) },
        external_resource: { url: urlValidator, maxLength: maxLength(2000) },
        sprint: {},
        start_date: { requiredIfSprint: requiredIf(this.sprint) },
        end_date: {
          requiredIfSprint: requiredIf(this.sprint),
          outOfSprint: (value, siblings) => {
            return (
              !helpers.req(value) ||
              !helpers.req(siblings.sprint) ||
              DateTime.fromISO(value) <= DateTime.fromISO(siblings.sprint.end_date)
            );
          },
          endDateBeforeStartDate: (value, siblings) => {
            return (
              !helpers.req(value) ||
              !helpers.req(siblings.start_date) ||
              DateTime.fromISO(siblings.start_date) <= DateTime.fromISO(value)
            );
          },
        },
        planned_effort: { required, numeric, minValue: minValue(1) },
        priority: { required, numeric, between: between(1, 10) },
        development_user: {},
        development_comments: { maxLength: maxLength(2000) },
        cvs_branch_name: { maxLength: maxLength(255) },
        cvs_issue_id: { numeric, minValue: minValue(1) },
        cvs_pull_request_id: { numeric, minValue: minValue(1) },
        validation_comments: { maxLength: maxLength(2000) },
        support_comments: { maxLength: maxLength(2000) },
        risk_level: { required },
        risk_comments: { maxLength: maxLength(2000) },
        use_migrations: { required },
        deployment_notes: { maxLength: maxLength(2000) },
      },
    };
  },
  setup(props) {
    // Store
    const mainStore = useMainStore();
    const userStoryStore = useUserStoryStore();

    // Composables
    const { copy: copyToClipboard, isSupported: isClipboardSupported } = useClipboard({ read: false });
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(UserStoryService, {
      buildSaveFunctionArgs,
      successMessage: "Historia de usuario guardada correctamente",
      customErrorMsgs: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
        outOfSprint: "Fecha fuera del sprint",
        requiredIfSprint: "Requerido si hay sprint",
      },
    });
    const { userStoryTypes: userStoryTypesOptions } = useUserStoryTypes();

    // State
    const epicService = EpicService;
    const sprintService = SprintService;
    const useMigrationsOptions = [
      { value: false, text: "No" },
      { value: true, text: "Sí" },
    ];
    const cvsVendor = defaultTo(userStoryStore.cvsVendor, "git");

    // Computed
    const { currentUser } = toRefs(mainStore);
    const { riskLevels: riskLevelOptions } = toRefs(userStoryStore);
    const canEdit = computed(() => {
      const action = item.value.id ? "change" : "add";
      return userHasPermission(`scrum.${action}_userstory`);
    });
    const hasARole = computed(() => {
      return [item.value.development_user, item.value.validation_user, item.value.support_user].includes(
        currentUser.value.id
      );
    });
    const validatedOptions = computed(() => {
      const canValidate = canEdit.value || item.value.validation_user === currentUser.value.id;
      return [
        { value: null, text: "Sin validar", disabled: false },
        {
          value: false,
          text: "Rechazada",
          disabled: props.sourceItem.validated !== false && !canValidate,
        },
        {
          value: true,
          text: "Validada",
          disabled: props.sourceItem.validated !== true && !canValidate,
        },
      ];
    });
    const validatedHintText = computed(() => {
      if (item.value.validated !== null && item.value.validated === props.sourceItem.validated) {
        return `Última modificación: ${isoDateTimeToLocaleString(item.value.validated_changed)}`;
      }
      return undefined;
    });
    const branchUrl = computed(() => {
      if (userStoryStore.cvsBranchBaseUrl && item.value.cvs_branch_name) {
        return `${userStoryStore.cvsBranchBaseUrl}/${item.value.cvs_branch_name}`;
      }
      return null;
    });
    const issueUrl = computed(() => {
      if (userStoryStore.cvsIssueBaseUrl && item.value.cvs_issue_id) {
        return `${userStoryStore.cvsIssueBaseUrl}/${item.value.cvs_issue_id}`;
      }
      return null;
    });
    const pullRequestUrl = computed(() => {
      if (userStoryStore.cvsPullRequestBaseUrl && item.value.cvs_pull_request_id) {
        return `${userStoryStore.cvsPullRequestBaseUrl}/${item.value.cvs_pull_request_id}`;
      }
      return null;
    });

    // Methods
    function buildSaveFunctionArgs(cleanedItem) {
      return [
        {
          ...cleanedItem,
          sprint: cleanedItem.sprint ? cleanedItem.sprint.id : null,
        },
        { expand: "sprint" },
      ];
    }
    function setStartDateFromSprint() {
      item.value.start_date = item.value.sprint ? item.value.sprint.start_date : null;
    }
    function setEndDateFromSprint() {
      item.value.end_date = item.value.sprint ? item.value.sprint.end_date : null;
    }
    function onSprintClear() {
      item.value.start_date = null;
      item.value.end_date = null;
    }
    function copyExternalResourceToClipboard() {
      try {
        copyToClipboard(item.value.external_resource);
        mainStore.showSnackbar({
          color: "info",
          message: "URI del recurso externo copiada al portapapeles",
        });
      } catch {
        mainStore.showSnackbar({
          color: "error",
          message: "Error copiando la URI del recurso externo al portapapeles",
        });
      }
    }

    return {
      // State
      item,
      epicService,
      sprintService,
      useMigrationsOptions,
      cvsVendor,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      isClipboardSupported,
      userStoryTypesOptions,
      currentUser,
      riskLevelOptions,
      canEdit,
      hasARole,
      validatedOptions,
      validatedHintText,
      branchUrl,
      issueUrl,
      pullRequestUrl,
      // Methods
      getErrorMsgs,
      submit,
      reset,
      copyToClipboard,
      setStartDateFromSprint,
      setEndDateFromSprint,
      onSprintClear,
      copyExternalResourceToClipboard,
      isWebUri,
      isoDateTimeToLocaleString,
    };
  },
};
</script>

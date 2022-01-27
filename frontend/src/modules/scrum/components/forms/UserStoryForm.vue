<template>
  <v-form v-if="item" ref="itemForm" :disabled="isTaskLoading('submit')">
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
                  :error-messages="buildValidationErrorMessages($v.item.name)"
                  @input="$v.item.name.$touch()"
                  @blur="$v.item.name.$touch()"
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
                  :error-messages="buildValidationErrorMessages($v.item.type)"
                  @change="$v.item.type.$touch()"
                  @blur="$v.item.type.$touch()"
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
                  <template v-if="item.epic" #append-outer>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :to="{ name: 'epic-user-stories', params: { epicId: item.epic } }"
                          icon
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
                  :error-messages="buildValidationErrorMessages($v.item.functional_description)"
                  @input="$v.item.functional_description.$touch()"
                  @blur="$v.item.functional_description.$touch()"
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
                  :error-messages="buildValidationErrorMessages($v.item.technical_description)"
                  @input="$v.item.technical_description.$touch()"
                  @blur="$v.item.technical_description.$touch()"
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
                  :readonly="!canEdit && loggedUser.id !== item.development_user"
                  :error-messages="buildValidationErrorMessages($v.item.external_resource)"
                  @input="$v.item.external_resource.$touch()"
                  @blur="$v.item.external_resource.$touch()"
                >
                  <template #append>
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
                  <template v-if="item.sprint" #append-outer>
                    <v-tooltip bottom>
                      <template #activator="{ on: onTooltip, attrs: attrTooltip }">
                        <v-btn
                          v-bind="attrTooltip"
                          :to="{
                            name: 'sprint-user-stories',
                            params: { sprintId: item.sprint.id },
                          }"
                          icon
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
                <v-menu
                  v-model="showStartDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template #activator="{ on, attrs }">
                    <v-text-field
                      :value="item.start_date | date"
                      label="Fecha de inicio planificada"
                      prepend-icon="mdi-calendar-start"
                      readonly
                      :clearable="canEdit"
                      :error-messages="buildValidationErrorMessages($v.item.start_date)"
                      v-bind="attrs"
                      @click:clear="item.start_date = null"
                      @blur="$v.item.start_date.$touch()"
                      v-on="on"
                    >
                      <template #append>
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
                    </v-text-field>
                  </template>
                  <v-date-picker
                    v-model="item.start_date"
                    :disabled="!canEdit"
                    :locale="locale"
                    :locale-first-day-of-year="4"
                    first-day-of-week="1"
                    color="primary"
                    show-week
                    no-title
                    @input="showStartDatepicker = false"
                    @change="$v.item.start_date.$touch()"
                  />
                </v-menu>
              </v-col>
              <v-col cols="12" sm="6" lg="4">
                <v-menu
                  v-model="showEndDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template #activator="{ on, attrs }">
                    <v-text-field
                      :value="item.end_date | date"
                      label="Fecha límite"
                      prepend-icon="mdi-calendar-end"
                      readonly
                      :clearable="canEdit"
                      :error-messages="buildValidationErrorMessages($v.item.end_date)"
                      v-bind="attrs"
                      @click:clear="item.end_date = null"
                      @blur="$v.item.end_date.$touch()"
                      v-on="on"
                    >
                      <template #append>
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
                    </v-text-field>
                  </template>
                  <v-date-picker
                    v-model="item.end_date"
                    :disabled="!canEdit"
                    :locale="locale"
                    :locale-first-day-of-year="4"
                    first-day-of-week="1"
                    color="primary"
                    show-week
                    no-title
                    @input="showEndDatepicker = false"
                    @change="$v.item.end_date.$touch()"
                  />
                </v-menu>
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
                  :error-messages="buildValidationErrorMessages($v.item.planned_effort)"
                  @input="$v.item.planned_effort.$touch()"
                  @blur="$v.item.planned_effort.$touch()"
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
                  :error-messages="buildValidationErrorMessages($v.item.priority)"
                  @input="$v.item.priority.$touch()"
                  @blur="$v.item.priority.$touch()"
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
                          :error-messages="buildValidationErrorMessages($v.item.development_user)"
                          @change="$v.item.development_user.$touch()"
                          @blur="$v.item.development_user.$touch()"
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
                          :readonly="!canEdit && loggedUser.id !== item.development_user"
                          :error-messages="buildValidationErrorMessages($v.item.development_comments)"
                          @input="$v.item.development_comments.$touch()"
                          @blur="$v.item.development_comments.$touch()"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-text-field
                          v-model.trim="item.cvs_reference"
                          label="Referencia SCV"
                          counter="255"
                          prepend-icon="mdi-git"
                          :readonly="!canEdit && loggedUser.id !== item.development_user"
                          :error-messages="buildValidationErrorMessages($v.item.cvs_reference)"
                          @input="$v.item.cvs_reference.$touch()"
                          @blur="$v.item.cvs_reference.$touch()"
                        />
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
                          :readonly="!canEdit && loggedUser.id !== item.validation_user"
                          :error-messages="buildValidationErrorMessages($v.item.validation_comments)"
                          @input="$v.item.validation_comments.$touch()"
                          @blur="$v.item.validation_comments.$touch()"
                        />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-select
                          v-model="item.validated"
                          :items="validatedOptions"
                          :disabled="item.status < 3"
                          :readonly="!canEdit && ![item.development_user, item.validation_user].includes(loggedUser.id)"
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
                          :readonly="!canEdit && loggedUser.id !== item.support_user"
                          :error-messages="buildValidationErrorMessages($v.item.support_comments)"
                          @input="$v.item.support_comments.$touch()"
                          @blur="$v.item.support_comments.$touch()"
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
                  :error-messages="buildValidationErrorMessages($v.item.risk_level)"
                  @change="$v.item.risk_level.$touch()"
                  @blur="$v.item.risk_level.$touch()"
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
                  :error-messages="buildValidationErrorMessages($v.item.risk_comments)"
                  @input="$v.item.risk_comments.$touch()"
                  @blur="$v.item.risk_comments.$touch()"
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
                  :readonly="!canEdit && loggedUser.id !== item.development_user"
                  :error-messages="buildValidationErrorMessages($v.item.use_migrations)"
                  @change="$v.item.use_migrations.$touch()"
                  @blur="$v.item.use_migrations.$touch()"
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
                  :readonly="!canEdit && loggedUser.id !== item.development_user"
                  :error-messages="buildValidationErrorMessages($v.item.deployment_notes)"
                  @input="$v.item.deployment_notes.$touch()"
                  @blur="$v.item.deployment_notes.$touch()"
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
import { mapState } from "pinia";
import { DateTime } from "luxon";
import { between, helpers, maxLength, minValue, numeric, required, requiredIf } from "vuelidate/lib/validators";
import { isWebUri } from "valid-url";
import { useClipboard } from "@vueuse/core";

import FormMixin from "@/mixins/form-mixin";

import EpicService from "@/modules/scrum/services/epic-service";
import SprintService from "@/modules/scrum/services/sprint-service";
import UserStoryService from "@/modules/scrum/services/user-story-service";

import { useMainStore } from "@/stores/main";
import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import useUserStoryTypes from "@/modules/scrum/composables/useUserStoryTypes";
import { isoDateTimeToLocaleString, isoDateToLocaleString } from "@/utils/dates";
import { userHasPermission } from "@/utils/permissions";
import { urlValidator } from "@/utils/validation";

export default {
  name: "UserStoryForm",
  filters: {
    date: isoDateToLocaleString,
  },
  mixins: [FormMixin({ service: UserStoryService })],
  validations: {
    item: {
      name: { required, maxLength: maxLength(500) },
      type: { required },
      functional_description: { maxLength: maxLength(2000) },
      technical_description: { maxLength: maxLength(2000) },
      external_resource: { url: urlValidator, maxLength: maxLength(2000) },
      sprint: {},
      start_date: { requiredIfSprint: requiredIf("sprint") },
      end_date: {
        requiredIfSprint: requiredIf("sprint"),
        outOfSprint: (value, vm) => {
          return (
            !helpers.req(vm.end_date) ||
            !helpers.req(vm.sprint) ||
            DateTime.fromISO(vm.end_date) <= DateTime.fromISO(vm.sprint.end_date)
          );
        },
        endDateBeforeStartDate: (value, vm) => {
          return (
            !helpers.req(vm.end_date) ||
            !helpers.req(vm.start_date) ||
            DateTime.fromISO(vm.start_date) <= DateTime.fromISO(vm.end_date)
          );
        },
      },
      planned_effort: { required, numeric, minValue: minValue(1) },
      priority: { required, numeric, between: between(1, 10) },
      development_user: {},
      development_comments: { maxLength: maxLength(2000) },
      cvs_reference: { maxLength: maxLength(255) },
      validation_comments: { maxLength: maxLength(2000) },
      support_comments: { maxLength: maxLength(2000) },
      risk_level: { required },
      risk_comments: { maxLength: maxLength(2000) },
      use_migrations: { required },
      deployment_notes: { maxLength: maxLength(2000) },
    },
  },
  setup() {
    const { copy: copyToClipboard, isSupported: isClipboardSupported } = useClipboard({ read: false });
    const { userStoryTypes: userStoryTypesOptions } = useUserStoryTypes();
    return {
      isClipboardSupported,
      copyToClipboard,
      userStoryTypesOptions,
    };
  },
  data() {
    return {
      epicService: EpicService,
      sprintService: SprintService,
      showStartDatepicker: false,
      showEndDatepicker: false,
      useMigrationsOptions: [
        { value: false, text: "No" },
        { value: true, text: "Sí" },
      ],
      validationErrorMessages: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
        outOfSprint: "Fecha fuera del sprint",
        requiredIfSprint: "Requerido si hay sprint",
      },
      successMessage: "Historia de usuario guardada correctamente",
    };
  },
  computed: {
    ...mapState(useMainStore, ["locale", "loggedUser"]),
    ...mapState(useUserStoryStore, {
      riskLevelOptions: "riskLevels",
    }),
    canEdit() {
      const action = this.item.id ? "change" : "add";
      return userHasPermission(`scrum.${action}_userstory`);
    },
    hasARole() {
      return [this.item.development_user, this.item.validation_user, this.item.support_user].includes(
        this.loggedUser.id
      );
    },
    validatedOptions() {
      const canValidate = this.canEdit || this.item.validation_user === this.loggedUser.id;
      return [
        { value: null, text: "Sin validar", disabled: false },
        {
          value: false,
          text: "Rechazada",
          disabled: this.sourceItem.validated !== false && !canValidate,
        },
        {
          value: true,
          text: "Validada",
          disabled: this.sourceItem.validated !== true && !canValidate,
        },
      ];
    },
    validatedHintText() {
      if (this.item.validated !== null && this.item.validated === this.sourceItem.validated) {
        return `Última modificación: ${isoDateTimeToLocaleString(this.item.validated_changed)}`;
      }
      return undefined;
    },
  },
  methods: {
    isWebUri,
    isoDateTimeToLocaleString,
    buildSaveFunctionArgs() {
      return [
        this.replaceUndefined({
          ...this.item,
          sprint: this.item.sprint ? this.item.sprint.id : null,
        }),
        { expand: "sprint" },
      ];
    },
    setStartDateFromSprint() {
      this.item.start_date = this.item.sprint ? this.item.sprint.start_date : null;
    },
    setEndDateFromSprint() {
      this.item.end_date = this.item.sprint ? this.item.sprint.end_date : null;
    },
    onSprintClear() {
      this.item.start_date = null;
      this.item.end_date = null;
    },
    copyExternalResourceToClipboard() {
      try {
        this.copyToClipboard(this.item.external_resource);
        this.showSnackbar({
          color: "info",
          message: "URI del recurso externo copiada al portapapeles",
        });
      } catch {
        this.showSnackbar({
          color: "error",
          message: "Error copiando la URI del recurso externo al portapapeles",
        });
      }
    },
  },
};
</script>

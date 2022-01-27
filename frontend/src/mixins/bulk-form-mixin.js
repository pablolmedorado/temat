import { mapActions } from "pinia";
import { validationMixin } from "vuelidate";
import { forOwn } from "lodash";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import { buildValidationErrorMessages, validationErrorMessages } from "@/utils/validation";

export default function BulkFormMixin({ service }) {
  if (!service) {
    throw new Error("service param is mandatory");
  }

  return {
    mixins: [validationMixin],
    props: {
      sourceItems: {
        type: Array,
        required: true,
      },
    },
    setup() {
      const { isLoading, addTask, removeTask, isTaskLoading } = useLoading();
      return {
        isLoading,
        addTask,
        removeTask,
        isTaskLoading,
      };
    },
    data() {
      return {
        validationErrorMessages,
        service,
        saveFunctionName: "save",
        items: this.sourceItems,
        successMessage: "Elementos guardados correctamente",
      };
    },
    watch: {
      sourceItems: {
        handler(newValue) {
          this.items = newValue;
        },
        deep: true,
      },
    },
    methods: {
      ...mapActions(useMainStore, ["showSnackbar"]),
      buildValidationErrorMessages,
      buildSaveFunctionArgs() {
        return [this.items.map((item) => this.replaceUndefined(item))];
      },
      reset() {
        this.$v.$reset();
        this.item = this.sourceItems;
      },
      async submit() {
        this.$v.$touch();
        if (this.$v.$invalid) {
          this.showSnackbar({
            color: "error",
            message: "El formulario contiene errores",
          });
          return null;
        } else {
          this.addTask("submit");
          try {
            const response = await this.service[this.saveFunctionName](...this.buildSaveFunctionArgs());
            this.showSnackbar({
              color: "success",
              message: this.successMessage,
            });
            return response.data;
          } finally {
            this.removeTask("submit");
          }
        }
      },
      replaceUndefined(item) {
        const newItem = { ...item };
        forOwn(newItem, (value, key, item) => {
          if (value === undefined) {
            item[key] = null;
          }
        });
        return newItem;
      },
    },
  };
}

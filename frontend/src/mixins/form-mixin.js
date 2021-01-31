import { mapActions } from "vuex";
import { validationMixin } from "vuelidate";
import { cloneDeep, difference, forOwn, isArray, isEqualWith } from "lodash";

import { buildValidationErrorMessages, validationErrorMessages } from "@/utils/validation";

export default function FormMixin({ service }) {
  if (!service) {
    throw new Error("service param is mandatory");
  }

  return {
    mixins: [validationMixin],
    props: {
      sourceItem: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        validationErrorMessages,
        service,
        saveFunctionName: "save",
        item: this.initializeItem(this.sourceItem),
        successMessage: "Elemento guardado correctamente",
      };
    },
    computed: {
      itemHasChanged() {
        return !isEqualWith(this.sourceItem, this.item, (sourceValue, currentValue) => {
          if (isArray(sourceValue) && isArray(currentValue)) {
            return difference(sourceValue, currentValue).length == 0;
          }
        });
      },
    },
    watch: {
      sourceItem(newValue) {
        this.item = this.initializeItem(newValue);
      },
      itemHasChanged: {
        handler(newValue) {
          this.$emit("changed:item", newValue);
        },
        immediate: true,
      },
    },
    methods: {
      ...mapActions(["showSnackbar"]),
      buildValidationErrorMessages,
      initializeItem(newItem) {
        return cloneDeep(newItem);
      },
      buildSaveFunctionArgs() {
        return [this.replaceUndefined(this.item)];
      },
      reset() {
        this.$v.$reset();
        this.item = this.initializeItem(this.sourceItem);
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
          const response = await this.service[this.saveFunctionName](...this.buildSaveFunctionArgs());
          this.showSnackbar({
            color: "success",
            message: this.successMessage,
          });
          return response.data;
        }
      },
      removeItemFromList(item, list) {
        const index = this.item[list].indexOf(item.id);
        if (index >= 0) {
          this.item[list].splice(index, 1);
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

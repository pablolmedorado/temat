// eslint-disable-next-line import/no-named-as-default
import useVuelidate from "@vuelidate/core";
import { isFunction } from "lodash-es";

export const defaultErrorMsgs = {
  between: ({ min, max }) => `Sólo valores entre ${min} y ${max}`,
  maxLength: ({ max }) => `Longitud máxima ${max}`,
  maxValue: ({ max }) => `Valor máximo ${max}`,
  minLength: ({ min }) => `Longitud mínima ${min}`,
  minValue: ({ min }) => `Valor mínimo ${min}`,
  numeric: "Valor numérico",
  required: "Campo requerido",
  url: "Formato de URL incorrecto",
};

export function useValidations(options = {}) {
  // Default options
  const { customErrorMsgs } = options;

  // Composables
  const v$ = useVuelidate({ $lazy: true, $autoDirty: true });

  // State
  const errorMsgs = {
    ...defaultErrorMsgs,
    ...customErrorMsgs,
  };

  // Methods
  function getErrorMsgs(property) {
    return property.$errors.map((error) => {
      const msg = errorMsgs[error.$validator] || error.$message;
      const actualMsg = isFunction(msg) ? msg(error.$params) : msg;
      return actualMsg || "[Mensaje de error no disponible]";
    });
  }

  return {
    v$,
    // State
    errorMsgs,
    // Methods
    getErrorMsgs,
  };
}

import { renderWithVuetify } from "@/utils/tests";

import Component from "@/components/TruncatedText";

test("truncates the text given in the prop", async () => {
  const { getByText } = renderWithVuetify(Component, {
    props: {
      value: "Lorem fistrum caballo blanco caballo negroorl",
    },
  });
  getByText("Lorem fistrum caballo...");
});

test("truncates the text given in the slot", async () => {
  const { getByText } = renderWithVuetify(Component, {
    slots: {
      default: "<template>Lorem fistrum caballo blanco caballo negroorl</template>",
    },
  });
  getByText("Lorem fistrum caballo...");
});

test("truncates the text using a custom length", async () => {
  const { getByText } = renderWithVuetify(Component, {
    props: {
      value: "Lorem fistrum caballo blanco caballo negroorl",
      textLength: 10,
    },
  });
  getByText("Lorem...");
});

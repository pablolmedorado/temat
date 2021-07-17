// Utilities
import { storyFactory } from "../../util/helpers";
import { text, number } from "@storybook/addon-knobs";

// Components
import TruncatedText from "@/components/TruncatedText";

export default { title: "Components/Common/TruncatedText" };

const story = storyFactory({ TruncatedText });

const buildProps = () => ({
  value: {
    default: text(
      "Value",
      "Lorem fistrum llevame al sircoo diodeno apetecan llevame al sircoo. A gramenawer te va a hasé pupitaa benemeritaar la caidita ese que llega condemor hasta luego Lucas la caidita se calle ustée te voy a borrar el cerito mamaar."
    ),
  },
  textLength: {
    default: number("Text length", 30),
  },
});

export const UsingProp = () =>
  story({
    props: buildProps(),
    template: `
      <TruncatedText :value="value" :text-length="textLength"></TruncatedText>
    `,
  });

export const UsingSlot = () =>
  story({
    props: buildProps(),
    template: `
      <TruncatedText :text-length="textLength">{{ value }}</TruncatedText>
    `,
  });

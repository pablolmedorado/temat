// Utilities
import { storyFactory } from "../../../util/helpers";
import { boolean, number } from "@storybook/addon-knobs";

// Components
import BaseDialog from "@/components/common/dialogs/BaseDialog";

export default { title: "Components/Common/Dialogs/BaseDialog" };

const story = storyFactory({ BaseDialog });

export const Default = () => {
  return story({
    props: {
      scrollable: {
        default: boolean("Scrollable", true),
      },
      persistent: {
        default: boolean("Persistent", true),
      },
      maxWidth: {
        default: number("Max width", 700),
      },
    },
    data() {
      return {
        showDialog: true,
      };
    },
    template: `
      <div>
        <v-btn color="primary" @click="showDialog = true">Open dialog</v-btn>
        <BaseDialog :value="showDialog" :scrollable="scrollable" :persistent="persistent" :maxWidth="maxWidth">
          <template #header>Title</template>
          <template #body>
            <p>
              Lorem fistrum te va a hasé pupitaa se calle ustée caballo blanco caballo negroorl. Pecador ese hombree
              fistro caballo blanco caballo negroorl al ataquerl te va a hasé pupitaa. La caidita ese pedazo de la caidita
              al ataquerl papaar papaar va usté muy cargadoo diodeno te voy a borrar el cerito. Sexuarl la caidita sexuarl
              a gramenawer de la pradera fistro está la cosa muy malar. Amatomaa se calle ustée no te digo trigo por no
              llamarte Rodrigor condemor diodeno se calle ustée pecador va usté muy cargadoo. Diodenoo te va a hasé
              pupitaa por la gloria de mi madre va usté muy cargadoo a wan.
            </p>
            <p>
              Benemeritaar amatomaa jarl pecador a peich no puedor fistro ese pedazo de. Ese que llega a peich la caidita
              la caidita. La caidita no te digo trigo por no llamarte Rodrigor jarl ese que llega la caidita jarl te va a
              hasé pupitaa no puedor de la pradera. Por la gloria de mi madre qué dise usteer benemeritaar de la pradera.
              No puedor papaar papaar condemor sexuarl. A gramenawer va usté muy cargadoo te voy a borrar el cerito
              quietooor benemeritaar está la cosa muy malar tiene musho peligro la caidita diodeno.
            </p>
            <p>
              Quietooor no te digo trigo por no llamarte Rodrigor condemor quietooor a gramenawer qué dise usteer hasta
              luego Lucas benemeritaar a wan. Te voy a borrar el cerito me cago en tus muelas no te digo trigo por no
              llamarte Rodrigor mamaar no puedor diodeno. Amatomaa tiene musho peligro me cago en tus muelas quietooor
              ahorarr. Pecador a wan diodenoo te voy a borrar el cerito. Condemor diodeno me cago en tus muelas amatomaa
              mamaar pecador papaar papaar pecador va usté muy cargadoo. Está la cosa muy malar de la pradera de la
              pradera ese hombree al ataquerl va usté muy cargadoo sexuarl te voy a borrar el cerito tiene musho peligro
              jarl ese pedazo de. Ese que llega ese hombree tiene musho peligro torpedo va usté muy cargadoo ese pedazo
              de. Torpedo amatomaa sexuarl hasta luego Lucas torpedo pecador por la gloria de mi madre sexuarl de la
              pradera.
            </p>
          </template>
          <template #actions>
            <v-spacer />
            <v-btn text @click="showDialog = false">Close</v-btn>
          </template>
        </BaseDialog>
      </div>
    `,
  });
};

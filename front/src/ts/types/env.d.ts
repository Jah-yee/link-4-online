declare module "*.vue" {
    import type { DefineComponent } from "vue";
    const components: DefineComponent<{},{},any>
    export default components
}
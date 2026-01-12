import type { Writable } from 'svelte/store'
import type { i18n as i18nType } from 'i18next'

declare module 'svelte' {
  export function getContext(key: 'i18n'): Writable<i18nType>
}

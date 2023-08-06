import { View } from 'backbone'
import { clickOpenModal } from 'helpers/Modal'

const CarouselItem = View.extend({
    initialize () {
      this.$button = this.$('add_crousel_item')
    },
})

export default CarouselItem

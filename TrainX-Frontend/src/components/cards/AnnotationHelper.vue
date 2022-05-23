<template>
	<mark :class="[tooltip, setMarkClass()]" @mouseover="mouseEnter" @mouseleave="mouseLeave">
		<slot></slot><div class="tooltiptext" v-if="hover">
			<v-btn @click.native="removeAnnotation" icon title="Delete annotation" class="delete-button">
				<v-icon>delete</v-icon>
			</v-btn>
			<input type="text" :placeholder="annotation.text" @input="updateUserQuery" />
			<div class="list-container">
				<ul v-for="result in elasticResults" :key="result.cui">
					<li v-if="resultIncludesUserQuery(result)" @click="setRefIdAndUpdateAnnotationSource(result.cui)" :class="[listItem, annotation.refId == result.cui ? active : '']">
						<p>{{ `${result.names[0] ? result.names[0] : ''} (${result.cui}) - ${result.semantic_type}` }}</p>
					</li>
				</ul>
			</div>
		</div>
	</mark>
</template>

<script>
export default {
	name: 'AnnotationHelper',

	props: {
		annotation: Object
	},

	data() {
		return {
			hover: false,
			updateElasticSearch: true,
			tooltip: 'tooltip',
			userAnnotation: 'userAnnotation',
			predictionAnnotation: 'predictionAnnotation',
			listItem: 'listItem',
			active: 'active'
		}
	},

	computed: {
		elasticResults () {
			let reorderedResults = this.$store.getters['elasticsearch/elasticResults'] && this.$store.getters['elasticsearch/elasticResults'].sort(item => {
				if (item.cui == this.$props.annotation.refId) { return -1 }
			})
			return reorderedResults
		},
	},

	methods: {
		setMarkClass () {
			if (this.$props.annotation.source === 'USER') return this.userAnnotation
			if (this.$props.annotation.source === 'PRED') return this.predictionAnnotation
		},

		dispatchElasticSearch (query) {			
			this.$store.dispatch('elasticsearch/getElasticResults', {
				text: query ? query : this.$props.annotation.text,
				refId: this.$props.annotation.refId,
				language: this.$store.getters['samples/samples'][0].language
			})
		},

		mouseEnter () {			
			this.hover = true
			if (this.updateElasticSearch) {
				this.dispatchElasticSearch()
				this.updateElasticSearch = false
			}
		},

		mouseLeave () {
			this.hover = false
			this.resetUserQuery()
			this.updateElasticSearch = true
			this.removeAnnotationIfNoRefIdIsSet()
		},

		updateUserQuery (e) {			
			let query = e.target.value || this.$props.annotation.text
			this.dispatchElasticSearch(query)			
		},

		resetUserQuery () {
			this.$store.commit('setUserQuery', '')
		},

		resultIncludesUserQuery (result) {
			let query = this.$store.getters.userQuery.trim().toLowerCase()
			return result.cui.toLowerCase().includes(query) || result.names[0].toLowerCase().includes(query) || result.semantic_type.toLowerCase().includes(query)
		},

		setRefIdAndUpdateAnnotationSource (refId) {
			this.$store.commit('samples/setRefId', {'refId': refId, 'annotation': this.annotation})
			this.$props.annotation.source = 'USER'
		},

		removeAnnotation () {
			this.$store.commit('samples/deleteAnnotation', this.annotation)
		},

		removeAnnotationIfNoRefIdIsSet() {
			if (!this.$props.annotation.refId) this.removeAnnotation()
		}
	},
}
</script>

<style scoped lang="scss">
	$tooltip-width: 260px;
	$tooltip-color: rgba(65, 86, 121, 0.9);
	$item-color: #ebf0f4;

	.userAnnotation {
		background-color: green;
	}

	.predictionAnnotation {
		background-color: rgb(129, 173, 255);
	}

	.delete-button {
		float: right;
		height: 24px;
		width: 24px;
		color: $item-color;
	}

	.tooltip {
		position: relative;
		display: inline-block;
	}

	.tooltiptext {
		position: absolute;
		top: 101%;
		left: 50%;
		height: auto;
		z-index: 1;
		width: $tooltip-width;
		margin-left: (-$tooltip-width)/2;
		background-color: $tooltip-color;
		padding: 8px;
		border-radius: 4px;
	}

	.tooltiptext::after {
		content: " ";
		position: absolute;
		bottom: 100%;
		left: 50%;
		margin-left: -5px;
		border-width: 5px;
		border-style: solid;
		border-color: transparent transparent $tooltip-color transparent;
	}

	input {
		width: 100%;
		height: 32px;
		border-radius: 4px;
		padding-left: 8px;
		margin-bottom: 4px;
		background-color: $item-color;
		color: black;
	}

	.list-container {
		position: relative;
		max-height: $tooltip-width*1.4;
		overflow-y: scroll;
		> ul {
			list-style-type: none;
			padding-left: 0;
		}
	}

	.listItem {
		background-color: rgba(183, 191, 207, 0.9);
		margin: 6px 0 6px 0;
		padding: 4px;
		border-radius: 4px;
	}

	div > ul > li:hover {
		background-color: $item-color;
	}

	.active {
		border: 2px solid peru;
		background-color: $item-color;
	}

	div > ul > li:last-of-type {
		margin: 6px 0 0 0;
	}
</style>

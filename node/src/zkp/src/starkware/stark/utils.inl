#include "starkware/stark/utils.h"

#include <memory>
#include <utility>

#include "starkware/commitment_scheme/commitment_scheme_builder.h"
#include "starkware/commitment_scheme/table_prover_impl.h"
#include "starkware/math/math.h"

namespace starkware {

template <typename FieldElementT>
TableProverFactory<FieldElementT> GetTableProverFactory(
    ProverChannel* channel, bool with_salt, Prng* prng) {
  return [channel, with_salt, prng](
             size_t n_segments, uint64_t n_rows_per_segment,
             size_t n_columns) -> std::unique_ptr<TableProver<FieldElementT>> {
    auto commitment_scheme = MakeCommitmentSchemeProver(
        FieldElementT::SizeInBytes() * n_columns, n_rows_per_segment, n_segments, channel,
        with_salt, prng);

    return std::make_unique<TableProverImpl<FieldElementT>>(
        n_columns, TakeOwnershipFrom(std::move(commitment_scheme)), channel);
  };
}

}  // namespace starkware

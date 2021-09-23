require 'rspec'

RSpec.describe 'our func' do
    it 'works for even nums [id]' do
        (2..10).step(2).each do |i|
            expect(is_even(i)).to eq(True)
        end
    end
end
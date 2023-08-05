depends = ('ITKPyBase', 'ITKCommon', )
templates = (
  ('FrequencyBandImageFilter', 'itk::FrequencyBandImageFilter', 'itkFrequencyBandImageFilterICF2', True, 'itk::Image< std::complex< float >,2 >'),
  ('FrequencyBandImageFilter', 'itk::FrequencyBandImageFilter', 'itkFrequencyBandImageFilterICF3', True, 'itk::Image< std::complex< float >,3 >'),
  ('FrequencyBandImageFilter', 'itk::FrequencyBandImageFilter', 'itkFrequencyBandImageFilterICF4', True, 'itk::Image< std::complex< float >,4 >'),
  ('UnaryFrequencyDomainFilter', 'itk::UnaryFrequencyDomainFilter', 'itkUnaryFrequencyDomainFilterICF2', True, 'itk::Image< std::complex< float >,2 >'),
  ('UnaryFrequencyDomainFilter', 'itk::UnaryFrequencyDomainFilter', 'itkUnaryFrequencyDomainFilterICF3', True, 'itk::Image< std::complex< float >,3 >'),
  ('UnaryFrequencyDomainFilter', 'itk::UnaryFrequencyDomainFilter', 'itkUnaryFrequencyDomainFilterICF4', True, 'itk::Image< std::complex< float >,4 >'),
)

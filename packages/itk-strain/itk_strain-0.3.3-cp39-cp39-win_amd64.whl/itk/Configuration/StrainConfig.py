depends = ('ITKPyBase', 'ITKImageSources', 'ITKImageGradient', 'ITKCommon', )
templates = (
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD22ISSRTD22', False, 'itk::Image< itk::Vector< double,2 >,2 >, itk::Image< itk::SymmetricSecondRankTensor< double, 2 >, 2 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD22ICVD22', False, 'itk::Image< itk::Vector< double,2 >,2 >, itk::Image< itk::CovariantVector< double,2 >,2 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD33ISSRTD33', False, 'itk::Image< itk::Vector< double,3 >,3 >, itk::Image< itk::SymmetricSecondRankTensor< double, 3 >, 3 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD33ICVD33', False, 'itk::Image< itk::Vector< double,3 >,3 >, itk::Image< itk::CovariantVector< double,3 >,3 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD44ISSRTD44', False, 'itk::Image< itk::Vector< double,4 >,4 >, itk::Image< itk::SymmetricSecondRankTensor< double, 4 >, 4 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIVD44ICVD44', False, 'itk::Image< itk::Vector< double,4 >,4 >, itk::Image< itk::CovariantVector< double,4 >,4 >'),
  ('StrainImageFilter', 'itk::StrainImageFilter', 'itkStrainImageFilterIVD22DD', True, 'itk::Image< itk::Vector< double,2 >,2 >, double, double'),
  ('StrainImageFilter', 'itk::StrainImageFilter', 'itkStrainImageFilterIVD33DD', True, 'itk::Image< itk::Vector< double,3 >,3 >, double, double'),
  ('StrainImageFilter', 'itk::StrainImageFilter', 'itkStrainImageFilterIVD44DD', True, 'itk::Image< itk::Vector< double,4 >,4 >, double, double'),
)
